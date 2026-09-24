"""SQLite Database Manager for Houston Business Listings.

Handles schema initialization, WAL mode optimization, batch upserts,
and full-text search indexing.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from .naics import get_naics_description, get_org_type_description


DEFAULT_DB_PATH = Path("houston_businesses.db")


class BusinessDatabase:
    """Manages SQLite storage and querying for Houston business records."""

    def __init__(self, db_path: Path = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        if self.conn is None:
            self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            # Performance PRAGMAs for massive ingestion
            self.conn.execute("PRAGMA journal_mode = WAL;")
            self.conn.execute("PRAGMA synchronous = NORMAL;")
            self.conn.execute("PRAGMA cache_size = -64000;")  # 64MB cache
            self.conn.execute("PRAGMA temp_store = MEMORY;")
        return self.conn

    def _init_db(self) -> None:
        """Create tables, indexes, and FTS5 full-text search."""
        conn = self._get_connection()
        with conn:
            # 1. Sales Tax Permits / Active Storefronts & DBAs
            conn.execute("""
                CREATE TABLE IF NOT EXISTS permits (
                    taxpayer_number TEXT NOT NULL,
                    taxpayer_name TEXT NOT NULL,
                    taxpayer_address TEXT,
                    taxpayer_city TEXT,
                    taxpayer_state TEXT,
                    taxpayer_zip TEXT,
                    taxpayer_county_code TEXT,
                    taxpayer_org_type TEXT,
                    org_type_desc TEXT,
                    outlet_number TEXT NOT NULL,
                    outlet_name TEXT NOT NULL,
                    outlet_address TEXT NOT NULL,
                    outlet_city TEXT NOT NULL,
                    outlet_state TEXT NOT NULL,
                    outlet_zip TEXT NOT NULL,
                    outlet_county_code TEXT,
                    outlet_naics_code TEXT,
                    naics_desc TEXT,
                    inside_city_limits TEXT,
                    permit_issue_date TEXT,
                    first_sales_date TEXT,
                    phone TEXT,
                    website TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (taxpayer_number, outlet_number)
                );
            """)

            # Indexes for permits
            conn.execute("CREATE INDEX IF NOT EXISTS idx_permits_zip ON permits (outlet_zip);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_permits_naics ON permits (outlet_naics_code);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_permits_name ON permits (outlet_name);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_permits_tp_name ON permits (taxpayer_name);")

            # 2. Franchise Taxpayers (Corporate Entities / LLCs / Corps)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS franchise_entities (
                    taxpayer_number TEXT PRIMARY KEY,
                    taxpayer_name TEXT NOT NULL,
                    taxpayer_address TEXT,
                    taxpayer_city TEXT,
                    taxpayer_state TEXT,
                    taxpayer_zip TEXT,
                    taxpayer_county_code TEXT,
                    org_type TEXT,
                    org_type_desc TEXT,
                    sos_file_number TEXT,
                    sos_charter_date TEXT,
                    sos_status_code TEXT,
                    right_to_transact_code TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.execute("CREATE INDEX IF NOT EXISTS idx_franchise_zip ON franchise_entities (taxpayer_zip);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_franchise_name ON franchise_entities (taxpayer_name);")

            # 3. Full-Text Search (FTS5) for Instant Multi-Field Lookup
            conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS permits_fts USING fts5(
                    outlet_name,
                    taxpayer_name,
                    outlet_address,
                    outlet_zip,
                    naics_desc,
                    content='permits',
                    content_rowid='rowid'
                );
            """)

            # Triggers to keep FTS index synchronized
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS permits_ai AFTER INSERT ON permits BEGIN
                    INSERT INTO permits_fts(rowid, outlet_name, taxpayer_name, outlet_address, outlet_zip, naics_desc)
                    VALUES (new.rowid, new.outlet_name, new.taxpayer_name, new.outlet_address, new.outlet_zip, new.naics_desc);
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS permits_ad AFTER DELETE ON permits BEGIN
                    INSERT INTO permits_fts(permits_fts, rowid, outlet_name, taxpayer_name, outlet_address, outlet_zip, naics_desc)
                    VALUES ('delete', old.rowid, old.outlet_name, old.taxpayer_name, old.outlet_address, old.outlet_zip, old.naics_desc);
                END;
            """)
            conn.execute("""
                CREATE TRIGGER IF NOT EXISTS permits_au AFTER UPDATE ON permits BEGIN
                    INSERT INTO permits_fts(permits_fts, rowid, outlet_name, taxpayer_name, outlet_address, outlet_zip, naics_desc)
                    VALUES ('delete', old.rowid, old.outlet_name, old.taxpayer_name, old.outlet_address, old.outlet_zip, old.naics_desc);
                    INSERT INTO permits_fts(rowid, outlet_name, taxpayer_name, outlet_address, outlet_zip, naics_desc)
                    VALUES (new.rowid, new.outlet_name, new.taxpayer_name, new.outlet_address, new.outlet_zip, new.naics_desc);
                END;
            """)

    def insert_permits_batch(self, records: List[Dict[str, Any]]) -> int:
        """Insert or replace a batch of sales tax permit records."""
        if not records:
            return 0

        conn = self._get_connection()
        rows = []
        for r in records:
            tp_num = r.get("taxpayer_number", "")
            out_num = r.get("outlet_number", "")
            if not tp_num or not out_num:
                continue

            naics_code = r.get("outlet_naics_code", "")
            org_code = r.get("taxpayer_organization_type", "")

            rows.append((
                tp_num,
                r.get("taxpayer_name", "").strip(),
                r.get("taxpayer_address", "").strip(),
                r.get("taxpayer_city", "").strip(),
                r.get("taxpayer_state", "").strip(),
                r.get("taxpayer_zip_code", "").strip(),
                r.get("taxpayer_county_code", "").strip(),
                org_code,
                get_org_type_description(org_code),
                out_num,
                r.get("outlet_name", "").strip(),
                r.get("outlet_address", "").strip(),
                r.get("outlet_city", "").strip(),
                r.get("outlet_state", "").strip(),
                r.get("outlet_zip_code", "").strip(),
                r.get("outlet_county_code", "").strip(),
                naics_code,
                get_naics_description(naics_code),
                r.get("outlet_inside_outside_city_limits_indicator", "").strip(),
                r.get("outlet_permit_issue_date", ""),
                r.get("outlet_first_sales_date", ""),
            ))

        with conn:
            conn.executemany("""
                INSERT OR REPLACE INTO permits (
                    taxpayer_number, taxpayer_name, taxpayer_address, taxpayer_city,
                    taxpayer_state, taxpayer_zip, taxpayer_county_code, taxpayer_org_type,
                    org_type_desc, outlet_number, outlet_name, outlet_address,
                    outlet_city, outlet_state, outlet_zip, outlet_county_code,
                    outlet_naics_code, naics_desc, inside_city_limits,
                    permit_issue_date, first_sales_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, rows)

        return len(rows)

    def insert_franchise_batch(self, records: List[Dict[str, Any]]) -> int:
        """Insert or replace a batch of franchise taxpayer records."""
        if not records:
            return 0

        conn = self._get_connection()
        rows = []
        for r in records:
            tp_num = r.get("taxpayer_number", "")
            if not tp_num:
                continue

            org_code = r.get("taxpayer_organizational_type", "")
            rows.append((
                tp_num,
                r.get("taxpayer_name", "").strip(),
                r.get("taxpayer_address", "").strip(),
                r.get("taxpayer_city", "").strip(),
                r.get("taxpayer_state", "").strip(),
                r.get("taxpayer_zip", "").strip(),
                r.get("taxpayer_county_code", "").strip(),
                org_code,
                get_org_type_description(org_code),
                r.get("secretary_of_state_sos_or_coa_file_number", "").strip(),
                r.get("sos_charter_date", ""),
                r.get("sos_status_code", "").strip(),
                r.get("right_to_transact_business_code", "").strip(),
            ))

        with conn:
            conn.executemany("""
                INSERT OR REPLACE INTO franchise_entities (
                    taxpayer_number, taxpayer_name, taxpayer_address, taxpayer_city,
                    taxpayer_state, taxpayer_zip, taxpayer_county_code, org_type,
                    org_type_desc, sos_file_number, sos_charter_date,
                    sos_status_code, right_to_transact_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, rows)

        return len(rows)

    def get_counts(self) -> Dict[str, int]:
        """Return the count of ingested permits and franchise entities."""
        conn = self._get_connection()
        c_permits = conn.execute("SELECT COUNT(*) FROM permits;").fetchone()[0]
        c_franchise = conn.execute("SELECT COUNT(*) FROM franchise_entities;").fetchone()[0]
        return {"permits": c_permits, "franchise": c_franchise, "total": c_permits + c_franchise}

    def search_fts(self, query: str, limit: int = 50) -> List[sqlite3.Row]:
        """Execute full-text search across permits."""
        conn = self._get_connection()
        # Clean query for FTS5 syntax
        clean_q = " ".join([f'"{token}"' for token in query.split() if token])
        return conn.execute("""
            SELECT p.* FROM permits p
            JOIN permits_fts f ON p.rowid = f.rowid
            WHERE permits_fts MATCH ?
            ORDER BY rank
            LIMIT ?;
        """, (clean_q, limit)).fetchall()

    def filter_permits(
        self,
        zip_code: Optional[str] = None,
        naics_prefix: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[sqlite3.Row]:
        """Filter permits by ZIP, NAICS prefix, or keyword."""
        conn = self._get_connection()
        clauses = ["1=1"]
        params: List[Any] = []

        if zip_code:
            clauses.append("outlet_zip LIKE ?")
            params.append(f"{zip_code}%")
        if naics_prefix:
            clauses.append("outlet_naics_code LIKE ?")
            params.append(f"{naics_prefix}%")
        if keyword:
            clauses.append("(outlet_name LIKE ? OR taxpayer_name LIKE ? OR outlet_address LIKE ?)")
            pattern = f"%{keyword}%"
            params.extend([pattern, pattern, pattern])

        sql = f"""
            SELECT * FROM permits
            WHERE {' AND '.join(clauses)}
            ORDER BY outlet_name ASC
            LIMIT ? OFFSET ?;
        """
        params.extend([limit, offset])
        return conn.execute(sql, params).fetchall()

    def get_top_industries(self, limit: int = 10) -> List[Tuple[str, str, int]]:
        """Return top NAICS industries by business count."""
        conn = self._get_connection()
        return conn.execute("""
            SELECT outlet_naics_code, naics_desc, COUNT(*) as count
            FROM permits
            WHERE outlet_naics_code IS NOT NULL AND outlet_naics_code != ''
            GROUP BY outlet_naics_code
            ORDER BY count DESC
            LIMIT ?;
        """, (limit,)).fetchall()

    def get_top_zip_codes(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Return top Houston ZIP codes by business count."""
        conn = self._get_connection()
        return conn.execute("""
            SELECT outlet_zip, COUNT(*) as count
            FROM permits
            WHERE outlet_zip IS NOT NULL AND outlet_zip != ''
            GROUP BY outlet_zip
            ORDER BY count DESC
            LIMIT ?;
        """, (limit,)).fetchall()

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
