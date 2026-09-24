"""Export Engine for Houston Business Data.

Streams database rows into CSV, JSON, and JSONL formats without loading
the entire dataset into memory.
"""

import csv
import json
import sqlite3
from pathlib import Path
from typing import Optional
from .database import BusinessDatabase


class DataExporter:
    """Exports SQLite records to portable file formats."""

    def __init__(self, db: BusinessDatabase):
        self.db = db

    def export_permits_csv(
        self,
        output_file: Path,
        zip_filter: Optional[str] = None,
        naics_filter: Optional[str] = None,
    ) -> int:
        """Stream permits into a clean, Excel-compatible CSV file."""
        output_path = Path(output_file)
        conn = self.db._get_connection()

        clauses = ["1=1"]
        params = []
        if zip_filter:
            clauses.append("outlet_zip LIKE ?")
            params.append(f"{zip_filter}%")
        if naics_filter:
            clauses.append("outlet_naics_code LIKE ?")
            params.append(f"{naics_filter}%")

        cursor = conn.execute(f"""
            SELECT 
                outlet_name,
                taxpayer_name,
                outlet_address,
                outlet_city,
                outlet_state,
                outlet_zip,
                outlet_naics_code,
                naics_desc,
                taxpayer_org_type,
                org_type_desc,
                permit_issue_date,
                first_sales_date,
                taxpayer_number,
                outlet_number
            FROM permits
            WHERE {' AND '.join(clauses)}
            ORDER BY outlet_name ASC;
        """, params)

        count = 0
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Business Name (DBA)",
                "Legal Taxpayer Name",
                "Street Address",
                "City",
                "State",
                "ZIP Code",
                "NAICS Code",
                "Industry Category",
                "Org Type Code",
                "Entity Structure",
                "Permit Issue Date",
                "First Sales Date",
                "Taxpayer Number",
                "Outlet Number"
            ])
            for row in cursor:
                writer.writerow(list(row))
                count += 1

        return count

    def export_permits_jsonl(
        self,
        output_file: Path,
        zip_filter: Optional[str] = None,
        naics_filter: Optional[str] = None,
    ) -> int:
        """Stream permits into JSON Lines (one JSON object per line)."""
        output_path = Path(output_file)
        conn = self.db._get_connection()

        clauses = ["1=1"]
        params = []
        if zip_filter:
            clauses.append("outlet_zip LIKE ?")
            params.append(f"{zip_filter}%")
        if naics_filter:
            clauses.append("outlet_naics_code LIKE ?")
            params.append(f"{naics_filter}%")

        cursor = conn.execute(f"""
            SELECT * FROM permits
            WHERE {' AND '.join(clauses)}
            ORDER BY outlet_name ASC;
        """, params)

        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for row in cursor:
                data = dict(row)
                f.write(json.dumps(data) + "\n")
                count += 1

        return count
