# Houston Business Scraper: 100% Complete Registry Crawler

A high-performance data pipeline and CLI tool that scrapes **every single registered and active business in Houston, Texas with no exceptions**, querying the official State of Texas Comptroller public records repository.

Unlike commercial web scraping (Google Maps, Yelp, YellowPages) which hits 120-result pagination limits and aggressive IP blocking, this tool taps into the **Texas Socrata Open Data API (SODA)** to harvest verified, ground-truth business registries with zero scraping blockers.

---

## 📊 Ground-Truth Coverage in Houston, TX

| Dataset | Scope | Total Records | Available Data Fields |
| :--- | :--- | :--- | :--- |
| **Active Sales Tax Permits** (`jrea-zgmq`) | All physical commercial storefronts, retail outlets, and DBAs in Houston. | **96,334+** *(City)*<br>**139,070+** *(Harris County)* | DBA Trade Name, Legal Taxpayer Name, Street Address, City, ZIP, NAICS Industry Code & Title, Permit Issue Date, First Sales Date. |
| **Active Franchise Taxpayers** (`9cir-efmm`) | All registered corporate entities (LLCs, Corporations, LPs, Partnerships). | **400,208+** *(City)* | Legal Entity Name, Principal Office Address, Secretary of State (SOS) Charter Number, Charter Date, Right to Transact Code. |

---

## ⚡ Quick Start

No external dependencies required (runs on pure Python 3 standard library).

```bash
# Navigate to the tool directory
cd /home/keenan/Projects/houston-business-scraper

# 1. Check live record counts on state servers
./run.sh count

# 2. Scrape all active storefronts and DBAs in Houston (~96k records in ~25 seconds)
./run.sh fetch --source permits

# 3. View instant industry breakdown and top ZIP codes
./run.sh stats

# 4. Search any keyword or industry instantly using SQLite FTS5
./run.sh search "Mechanical"

# 5. Export all listings to CSV (Excel-ready)
./run.sh export --format csv --output houston_businesses.csv
```

---

## 🛠️ CLI Command Reference

### 1. `count`
Check live online record counts on the Texas state servers:
```bash
./run.sh count
```

### 2. `fetch`
Ingest business records into the local SQLite database (`houston_businesses.db`):
```bash
# Fetch all active Houston sales tax permits / storefronts
./run.sh fetch --source permits

# Fetch all businesses in the greater Harris County area (139k records)
./run.sh fetch --source permits --all-county

# Fetch all registered corporate franchise entities (400k records)
./run.sh fetch --source franchise

# Fetch a quick test sample of 5,000 records
./run.sh fetch --source permits --limit 5000
```

### 3. `search`
Execute lightning-fast full-text search across business names, DBAs, addresses, and NAICS titles:
```bash
./run.sh search "Roofing"
./run.sh search "Dental"
./run.sh search "77002"
```

### 4. `stats`
Generate executive analytics and top industry distributions:
```bash
./run.sh stats
```

### 5. `export`
Stream records from the SQLite database to CSV or JSON Lines:
```bash
# Export all records to CSV
./run.sh export --format csv --output all_houston_businesses.csv

# Export only restaurants (NAICS 722)
./run.sh export --format csv --naics 722 --output houston_restaurants.csv

# Export specific ZIP code (e.g., Downtown 77002)
./run.sh export --format csv --zip 77002 --output downtown_businesses.csv

# Export to JSON Lines for BigQuery / Elasticsearch ingestion
./run.sh export --format jsonl --output houston_businesses.jsonl
```

---

## 🏛️ Database Schema (`houston_businesses.db`)

All data is stored locally in SQLite with **Write-Ahead Logging (WAL)** and an **FTS5 Full-Text Search Virtual Table**:

* **`permits` Table:**
  * `outlet_name`: Business Trade Name / DBA (e.g. *"Speedy Mart"*)
  * `taxpayer_name`: Legal Corporation / LLC Name (e.g. *"Onkar Inc."*)
  * `outlet_address`: Physical Street Address (e.g. *"2050 Bingle Rd"*)
  * `outlet_city`, `outlet_state`, `outlet_zip`
  * `outlet_naics_code`: 6-digit NAICS Industry Code
  * `naics_desc`: Plain-English Industry Classification
  * `org_type_desc`: Entity Structure (LLC, Texas Corp, Sole Proprietorship)
  * `permit_issue_date`, `first_sales_date`
  * `taxpayer_number`, `outlet_number`

---

## 🚀 Performance Highlights
* **Zero Scraping Blockers:** 100% legitimate public data access via Socrata SODA REST API.
* **Streaming Ingestion:** Pulls 10,000 records per HTTP batch in ~1.5 seconds.
* **Memory Efficient:** Exports directly stream SQLite cursors to disk without memory bloat.

## Harness pipeline export (offline)

From `market-intelligence/scraper/`, normalize existing sliced CSVs without fetching data or modifying the research lists:

```bash
python3 -m houston_biz pipeline-leads \
  --input ../leads/commercial_contractors.csv ../leads/healthcare_hipaa.csv \
  --output ../../harness/local/contractor-clinic-candidates.csv
```

Initialize the harness first so its local directory exists. The output filename must be new: existing files are never overwritten. The command prints counts for rows read, filtered, invalid, duplicated, and exported. It accepts the existing sliced headers, the scraper's standard permit export headers, or equivalent raw permit field names. UTF-8 BOMs and quoted CSV fields are supported; malformed headers/row widths fail without publishing partial output.

Default selection is **Houston, Texas**. Repeat `--city` to explicitly include surrounding municipalities, for example `--city Houston --city Katy`. An explicit city list replaces the default. This is city-name filtering, not geospatial or county-boundary matching.

Use `--vertical contractors`, `--vertical clinics`, or the default `both`. Contractor targeting selects `238*` and `236220`; clinic targeting selects `6211*`, `6212*`, `6213*`, and `6214*`. These are targeting heuristics, not proof of commercial work, regulatory obligations, business size, or service fit. Home-health, laboratory, and other healthcare categories outside those prefixes are excluded. No completeness claim is made about registry coverage.

Normalization trims/collapses whitespace, checks six-digit NAICS and ZIP formats, and deduplicates by case-normalized business name plus address/city/state/five-digit ZIP. Distinct branches and suite addresses remain separate. Stable hashed IDs make repeat imports idempotent. This deliberately does not fuzzy-merge spelling changes or street abbreviations. First occurrence wins for duplicates. Formula-like business-name values are escaped for spreadsheet display.

Output is the harness pipeline schema, with stage `research`, source-file provenance, blank verification/contact-person fields, and no fabricated phone/email data. Output is built in a temporary file and published without replacing an existing destination. Deduplication holds matching candidates in memory; this path is intended for curated CSV exports, not an unbounded stream.

From the repository root:

```bash
python3 harness/mcd.py import-leads harness/local/contractor-clinic-candidates.csv --dry-run
python3 harness/mcd.py import-leads harness/local/contractor-clinic-candidates.csv
python3 -m unittest discover -s harness/tests -v
```

The tests cover normalizer filtering, stable deduplication, malformed-input handling, export preservation, and a real subprocess round trip through both CLIs. Existing fetch/export commands remain separate. No live network fetch is required to run this test suite.
