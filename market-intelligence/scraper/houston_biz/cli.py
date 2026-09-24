"""Command-Line Interface for Houston Business Scraper.

Provides commands to fetch, search, filter, analyze, and export
business listings in Houston, Texas.
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional

from .client import DATASET_FRANCHISE, DATASET_PERMITS, SocrataClient
from .database import BusinessDatabase, DEFAULT_DB_PATH
from .exporter import DataExporter


def format_progress(current: int, total: int, prefix: str = "") -> None:
    """Print clean terminal progress counter."""
    percent = (current / total * 100) if total > 0 else 100.0
    sys.stdout.write(f"\r{prefix} [{current:,} / {total:,}] ({percent:.1f}%)")
    sys.stdout.flush()


def cmd_count(args: argparse.Namespace) -> None:
    """Query live online record counts from the Texas Comptroller."""
    print("Connecting to Texas Comptroller Open Data (data.texas.gov)...")
    client = SocrataClient()
    
    where_houston_permits = "upper(outlet_city)='HOUSTON'"
    where_harris_permits = "outlet_county_code='101'"
    where_houston_franchise = "upper(taxpayer_city)='HOUSTON'"

    permits_houston = client.get_count(DATASET_PERMITS, where_houston_permits)
    permits_harris = client.get_count(DATASET_PERMITS, where_harris_permits)
    franchise_houston = client.get_count(DATASET_FRANCHISE, where_houston_franchise)

    print("\n=======================================================")
    print("       LIVE STATE REGISTRY COUNTS FOR HOUSTON, TX       ")
    print("=======================================================")
    print(f" • Active Sales Tax Permits (City = HOUSTON):    {permits_houston:,} storefronts/outlets")
    print(f" • Active Sales Tax Permits (Harris County 101): {permits_harris:,} storefronts/outlets")
    print(f" • Active Franchise Taxpayers (City = HOUSTON): {franchise_houston:,} corporate entities")
    print("=======================================================\n")


def cmd_fetch(args: argparse.Namespace) -> None:
    """Scrape and store business listings from Texas Comptroller."""
    db = BusinessDatabase(Path(args.db))
    client = SocrataClient(app_token=args.app_token)
    source = args.source.lower()
    max_rec = args.limit if args.limit and args.limit > 0 else None
    chunk = args.chunk_size

    t0 = time.time()

    # 1. Fetch Sales Tax Permits (Physical Storefronts & DBAs)
    if source in ("permits", "all"):
        where = "upper(outlet_city)='HOUSTON'" if not args.all_county else "outlet_county_code='101'"
        total = client.get_count(DATASET_PERMITS, where)
        target = min(total, max_rec) if max_rec else total
        print(f"\n[+] Fetching {target:,} Active Sales Tax Permits ({'Harris County' if args.all_county else 'City of Houston'})...")

        retrieved = 0
        for batch in client.fetch_records_stream(
            DATASET_PERMITS,
            where=where,
            order_by="taxpayer_number,outlet_number",
            chunk_size=chunk,
            max_records=target,
        ):
            db.insert_permits_batch(batch)
            retrieved += len(batch)
            format_progress(retrieved, target, prefix=" -> Ingesting Permits:")
        print(f"\n[✓] Permits complete: {retrieved:,} records stored.")

    # 2. Fetch Franchise Taxpayers (Corporate Entities / LLCs / Corps)
    if source in ("franchise", "all"):
        where = "upper(taxpayer_city)='HOUSTON'"
        total = client.get_count(DATASET_FRANCHISE, where)
        target = min(total, max_rec) if max_rec else total
        print(f"\n[+] Fetching {target:,} Active Franchise Taxpayers (City of Houston)...")

        retrieved = 0
        for batch in client.fetch_records_stream(
            DATASET_FRANCHISE,
            where=where,
            order_by="taxpayer_number",
            chunk_size=chunk,
            max_records=target,
        ):
            db.insert_franchise_batch(batch)
            retrieved += len(batch)
            format_progress(retrieved, target, prefix=" -> Ingesting Franchise:")
        print(f"\n[✓] Franchise complete: {retrieved:,} records stored.")

    elapsed = round(time.time() - t0, 2)
    counts = db.get_counts()
    print(f"\n[★] Scraping complete in {elapsed}s!")
    print(f"    Database: {db.db_path} ({counts['permits']:,} permits, {counts['franchise']:,} franchise entities)\n")


def cmd_search(args: argparse.Namespace) -> None:
    """Perform full-text search across local database."""
    db = BusinessDatabase(Path(args.db))
    query = args.query
    results = db.search_fts(query, limit=args.limit)

    print(f"\nSearch Results for: \"{query}\" (Showing top {len(results)}):")
    print("-" * 80)
    for i, row in enumerate(results, 1):
        dba = row["outlet_name"]
        corp = row["taxpayer_name"]
        addr = f"{row['outlet_address']}, {row['outlet_city']}, {row['outlet_state']} {row['outlet_zip']}"
        naics = row["naics_desc"]
        print(f"{i:2d}. {dba} (Legal: {corp})")
        print(f"    Address:  {addr}")
        print(f"    Industry: [{row['outlet_naics_code']}] {naics}")
        print()


def cmd_stats(args: argparse.Namespace) -> None:
    """Display summary analytics and breakdown of scraped businesses."""
    db = BusinessDatabase(Path(args.db))
    counts = db.get_counts()

    print("\n=======================================================")
    print("           HOUSTON BUSINESS DATABASE STATS             ")
    print("=======================================================")
    print(f" • Active Permits (Storefronts/DBAs): {counts['permits']:,}")
    print(f" • Corporate Entities (Franchise):     {counts['franchise']:,}")
    print(f" • Total Records Indexed:              {counts['total']:,}")
    print("-" * 55)

    print("\nTop 10 Business Industries in Houston:")
    for code, desc, cnt in db.get_top_industries(10):
        print(f" • {cnt:6,d} | [{code}] {desc}")

    print("\nTop 10 ZIP Codes by Business Concentration:")
    for zip_code, cnt in db.get_top_zip_codes(10):
        print(f" • {zip_code}: {cnt:6,d} businesses")
    print("=======================================================\n")


def cmd_export(args: argparse.Namespace) -> None:
    """Export local database to CSV or JSONL."""
    db = BusinessDatabase(Path(args.db))
    exporter = DataExporter(db)
    out_file = Path(args.output)

    fmt = args.format.lower()
    print(f"[+] Exporting Houston businesses to {out_file} ({fmt.upper()})...")

    if fmt == "csv":
        count = exporter.export_permits_csv(out_file, zip_filter=args.zip, naics_filter=args.naics)
    elif fmt in ("jsonl", "json"):
        count = exporter.export_permits_jsonl(out_file, zip_filter=args.zip, naics_filter=args.naics)
    else:
        print(f"[!] Unsupported format: {fmt}")
        return

    print(f"[✓] Successfully exported {count:,} business records to {out_file}!\n")


def cmd_mssp_leads(args: argparse.Namespace) -> None:
    """Generate pre-sliced, compliance-tagged B2B lead lists for Managed Security Service Providers."""
    import csv
    db = BusinessDatabase(Path(args.db))
    conn = db._get_connection()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    verticals = {
        "healthcare_hipaa.csv": ("outlet_naics_code LIKE '621%'", "HIPAA / HITECH Patient Data Protection & Ransomware Defense"),
        "commercial_contractors.csv": ("outlet_naics_code LIKE '238%'", "Business Email Compromise (BEC) & Cyber Insurance Renewal"),
        "engineering_cmmc.csv": ("outlet_naics_code LIKE '5413%'", "CMMC 2.0 / Proprietary CAD & IP Protection"),
        "oil_gas_energy.csv": ("outlet_naics_code LIKE '211%' OR outlet_naics_code LIKE '213%' OR outlet_naics_code LIKE '333132'", "Enterprise Operator Vendor Cybersecurity Audits"),
        "law_firms_legal.csv": ("outlet_naics_code LIKE '5411%'", "State Bar Ethics / Client Wire Fraud / Escrow Defense"),
        "cpa_accounting.csv": ("outlet_naics_code LIKE '5412%'", "FTC Safeguards Rule / Taxpayer PII Protection"),
        "logistics_maritime.csv": ("outlet_naics_code LIKE '484%' OR outlet_naics_code LIKE '493%'", "Supply Chain / Port Operations Business Continuity"),
    }

    print("\n=======================================================")
    print("      HOUSTON MSSP B2B LEAD GENERATION ENGINE          ")
    print("=======================================================")
    total = 0
    for filename, (clause, hook) in verticals.items():
        file_path = out_dir / filename
        rows = conn.execute(f"""
            SELECT 
                outlet_name AS business_name,
                taxpayer_name AS legal_name,
                outlet_address AS address,
                outlet_city AS city,
                outlet_state AS state,
                outlet_zip AS zip_code,
                outlet_naics_code AS naics,
                naics_desc AS industry,
                org_type_desc AS entity_type,
                permit_issue_date AS permit_date,
                '{hook}' AS regulatory_sales_hook
            FROM permits
            WHERE {clause}
            ORDER BY outlet_name ASC;
        """).fetchall()

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Business / DBA Name", "Legal Entity Name", "Street Address", "City",
                "State", "ZIP Code", "NAICS Code", "Industry Category", "Entity Type",
                "Permit Issue Date", "MSSP Regulatory Sales Hook"
            ])
            for r in rows:
                writer.writerow(list(r))

        print(f" • {filename:26s} : {len(rows):5,d} leads -> {file_path.name}")
        total += len(rows)

    print("-" * 55)
    print(f"[✓] Total Qualified Houston MSSP Leads: {total:,}")
    print(f"    Saved into directory: {out_dir.resolve()}\n")



def main() -> None:
    parser = argparse.ArgumentParser(
        description="Houston Business Scraper: 100% comprehensive public business intelligence for Houston, TX."
    )
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to SQLite database")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: count
    subparsers.add_parser("count", help="Check live total business counts on Texas State servers")

    # Command: fetch
    p_fetch = subparsers.add_parser("fetch", help="Scrape business listings into local SQLite database")
    p_fetch.add_argument("--source", choices=["permits", "franchise", "all"], default="permits",
                         help="Data source (permits = storefronts/DBAs, franchise = corporate entities, all = both)")
    p_fetch.add_argument("--limit", type=int, default=None, help="Maximum records to fetch (default: all)")
    p_fetch.add_argument("--chunk-size", type=int, default=10000, help="Batch size per HTTP request (default: 10,000)")
    p_fetch.add_argument("--all-county", action="store_true", help="Include all Harris County (101) instead of just Houston city limits")
    p_fetch.add_argument("--app-token", default=None, help="Optional Socrata App Token for higher rate limits")

    # Command: search
    p_search = subparsers.add_parser("search", help="Full-text search in local database")
    p_search.add_argument("query", help="Keyword to search (business name, DBA, address, or NAICS)")
    p_search.add_argument("--limit", type=int, default=20, help="Maximum search results to display")

    # Command: stats
    subparsers.add_parser("stats", help="Display industry and ZIP code breakdown")

    # Command: export
    p_export = subparsers.add_parser("export", help="Export businesses to CSV or JSONL")
    p_export.add_argument("--format", choices=["csv", "jsonl"], default="csv", help="Export file format")
    p_export.add_argument("--output", default="houston_businesses.csv", help="Output file path")
    p_export.add_argument("--zip", default=None, help="Optional ZIP code filter prefix (e.g. 77002)")
    p_export.add_argument("--naics", default=None, help="Optional NAICS code filter prefix (e.g. 722 for food)")

    # Command: mssp-leads
    p_mssp = subparsers.add_parser("mssp-leads", help="Generate pre-sliced MSSP B2B lead lists across 7 high-value target verticals")
    p_mssp.add_argument("--output-dir", default="leads", help="Output directory for sliced lead CSVs (default: leads/)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "count":
        cmd_count(args)
    elif args.command == "fetch":
        cmd_fetch(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "mssp-leads":
        cmd_mssp_leads(args)


if __name__ == "__main__":
    main()
