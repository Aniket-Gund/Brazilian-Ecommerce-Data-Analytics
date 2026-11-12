# Olist BI Architecture: Step-by-Step Setup & Reproduction Guide

This guide walks through reproducing the entire hybrid multi-cloud Business Intelligence environment from scratch on Windows PowerShell.

---

## 1. Prerequisites
* **Python 3.10+** (tested on Python 3.13)
* **Power BI Desktop** (latest release)
* Free **Supabase** account ([supabase.com](https://supabase.com))
* Free **Google Cloud Platform (GCP)** account with BigQuery Sandbox

---

## 2. Python Environment Setup
Open Windows PowerShell in the project directory:

```powershell
# 1. Create Python virtual environment
python -m venv venv

# 2. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip and install all project dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Cloud Credentials Configuration (`.env`)
Create a `.env` file in the root directory:

```env
SUPABASE_DB_URL=postgresql://postgres.[YOUR-PROJECT-REF]:[YOUR-PASSWORD]@aws-0-eu-north-1.pooler.supabase.com:5432/postgres
```
*(Make sure to use the IPv4 Session Pooler host `aws-0-[region].pooler.supabase.com:5432` to avoid IPv6 resolution timeouts on local ISP networks).*

---

## 4. Google BigQuery Service Account Setup
1. In Google Cloud Console, create a new project: `golden-toolbox-431720-i9`.
2. Enable the **BigQuery API**.
3. Create a Service Account with the **BigQuery Admin** role.
4. Generate a JSON Key and save it as:
   `docs/gcp_service_account.json`

---

## 5. End-to-End Data Loading Pipeline
Execute the Python loading scripts to hydrate the cloud data tiers:

```powershell
# 1. Load 4 Fact tables to Supabase Cloud PostgreSQL
python scripts/load_supabase.py

# 2. Load 4 Dimension tables to Google BigQuery
python scripts/load_bigquery.py

# 3. Execute the 27-point unbreakability audit suite
python scripts/system_integrity_audit.py
```

---

## 6. Power BI Desktop Configuration
1. Launch **Power BI Desktop**.
2. **Critical Step:** Go to `File` $\rightarrow$ `Options and settings` $\rightarrow$ `Options` $\rightarrow$ `Current File` $\rightarrow$ `Data Load`:
   * **UNCHECK "Auto date/time"** (prevents hidden automatic calendar tables).
3. Connect Data Sources:
   * **Supabase PostgreSQL:** `Get Data` $\rightarrow$ `PostgreSQL Database` $\rightarrow$ Server: `aws-0-eu-north-1.pooler.supabase.com:5432` $\rightarrow$ Database: `postgres` $\rightarrow$ Authentication: Database (`postgres.[REF]` / Password) $\rightarrow$ Uncheck "Encrypt connections".
   * **Google BigQuery:** `Get Data` $\rightarrow$ `Google BigQuery` $\rightarrow$ Sign in via Google account $\rightarrow$ Select project dataset `olist_ecommerce`.
   * **Google Sheets:** `Get Data` $\rightarrow$ `Web` $\rightarrow$ Enter CSV export URLs for `category_translation` and `kpi_targets`.
4. Apply the Star Schema relationships and DAX formulas from `step7_dashboard_build_guide.md`.

---

## 7. Live Refresh & Simulation Testing
```powershell
# Ingest 500 new streaming transactions into PostgreSQL
python scripts/simulate_new_orders.py --orders 500

# Open Power BI Desktop and click 'Refresh' on the Home ribbon to observe live data absorption!
```
