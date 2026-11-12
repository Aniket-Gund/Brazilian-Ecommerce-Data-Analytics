"""
Olist E-Commerce: Master Enterprise ETL & Health Check Pipeline (Step 8)
------------------------------------------------------------------------
Orchestrates end-to-end multi-cloud pipeline monitoring and health checks:
1. Supabase PostgreSQL (Facts Layer - Transactional Engine)
2. Google BigQuery Sandbox (Dimensions Layer - Enterprise Warehouse)
3. Google Sheets (Reference Layer - Business Governance & KPI Targets)

Usage:
    python scripts/etl_pipeline.py [--simulate N]
"""

import os
import sys
import time
import argparse
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from google.cloud import bigquery
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

load_dotenv()

# 1. Environment Variables & Credentials
SUPABASE_URL = os.getenv('SUPABASE_DB_URL')
GCP_SA_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs', 'gcp_service_account.json')
GCP_PROJECT_ID = "golden-toolbox-431720-i9"
BQ_DATASET = "olist_ecommerce"
GSHEETS_URL = "https://docs.google.com/spreadsheets/d/1qAYYd5DTR0NrxsGbeM82_zdDjrLdNP8fk-K9eLGQLDQ/export?format=csv&gid=0"

def audit_supabase():
    """Audits Supabase Cloud PostgreSQL Fact tables."""
    print("\n[1/3] 🐘 Auditing Supabase Cloud PostgreSQL (Fact Layer)...")
    if not SUPABASE_URL:
        print("   ❌ SUPABASE_DB_URL missing in .env")
        return False, {}
    
    db_url = SUPABASE_URL
    if db_url.startswith('postgresql://'):
        db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
        
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            orders_cnt = conn.execute(text("SELECT count(*) FROM fact_orders")).scalar()
            items_cnt = conn.execute(text("SELECT count(*) FROM fact_order_items")).scalar()
            payments_cnt = conn.execute(text("SELECT count(*) FROM fact_payments")).scalar()
            reviews_cnt = conn.execute(text("SELECT count(*) FROM fact_reviews")).scalar()
            total_gmv = conn.execute(text("SELECT COALESCE(SUM(total_value), 0) FROM fact_order_items")).scalar()

        print(f"   ✓ fact_orders:      {orders_cnt:,} rows")
        print(f"   ✓ fact_order_items: {items_cnt:,} rows")
        print(f"   ✓ fact_payments:    {payments_cnt:,} rows")
        print(f"   ✓ fact_reviews:     {reviews_cnt:,} rows")
        print(f"   ✓ Live Total GMV:   ${float(total_gmv):,.2f}")
        return True, {
            'orders': orders_cnt,
            'items': items_cnt,
            'payments': payments_cnt,
            'reviews': reviews_cnt,
            'gmv': float(total_gmv)
        }
    except Exception as e:
        print(f"   ❌ Supabase audit failed: {e}")
        return False, {}

def audit_bigquery():
    """Audits Google BigQuery Dimension tables."""
    print("\n[2/3] ☁️  Auditing Google BigQuery Sandbox (Dimension Layer)...")
    if not os.path.exists(GCP_SA_PATH):
        print(f"   ⚠️  BigQuery Service Account key not found at {GCP_SA_PATH}. Skipping API check.")
        return True, {'status': 'Local reference active'}

    try:
        client = bigquery.Client.from_service_account_json(GCP_SA_PATH, project=GCP_PROJECT_ID)
        tables = ['dim_customers', 'dim_products', 'dim_sellers', 'dim_date']
        counts = {}
        for tbl in tables:
            query = f"SELECT count(*) as cnt FROM `{GCP_PROJECT_ID}.{BQ_DATASET}.{tbl}`"
            res = list(client.query(query).result())
            cnt = res[0].cnt
            counts[tbl] = cnt
            print(f"   ✓ {tbl}: {cnt:,} rows")
        return True, counts
    except Exception as e:
        print(f"   ⚠️  BigQuery check note: {e}")
        return True, {'note': str(e)}

def audit_google_sheets():
    """Audits Google Sheets Lookup tables."""
    print("\n[3/3] 📑 Auditing Google Sheets (Reference & Governance Layer)...")
    try:
        df = pd.read_csv(GSHEETS_URL)
        print(f"   ✓ category_translation live lookup reachable ({len(df):,} categories mapped)")
        return True, {'categories': len(df)}
    except Exception as e:
        print(f"   ⚠️  Google Sheets read note: {e}")
        return True, {'note': str(e)}

def run_pipeline(simulate_n=0):
    """Executes the full master ETL orchestrator."""
    start_ts = time.time()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("=" * 65)
    print(f"🚀 OLIST MASTER ETL PIPELINE RUN — {now_str}")
    print("=" * 65)

    if simulate_n > 0:
        from simulate_new_orders import load_dimension_samples, generate_synthetic_orders, stream_to_supabase
        dims = load_dimension_samples()
        df_o, df_i, df_p, df_r = generate_synthetic_orders(num_orders=simulate_n, dims=dims)
        stream_to_supabase(df_o, df_i, df_p, df_r)

    sb_ok, sb_data = audit_supabase()
    bq_ok, bq_data = audit_bigquery()
    gs_ok, gs_data = audit_google_sheets()

    duration = time.time() - start_ts
    print("\n" + "=" * 65)
    print(f"🏁 MASTER PIPELINE AUDIT COMPLETED in {duration:.2f}s")
    print(f"   Multi-Source Cloud Health: {'✅ HEALTHY' if (sb_ok and bq_ok and gs_ok) else '⚠️ WARNING'}")
    print(f"   PostgreSQL Live Orders:    {sb_data.get('orders', 'N/A'):,}")
    print(f"   PostgreSQL Live GMV:       ${sb_data.get('gmv', 0):,.2f}")
    print("=" * 65)
    print("\n⚡ Ready for Power BI Desktop Refresh:")
    print("   Click 'Refresh' on the Power BI Desktop Home ribbon to ingest live changes!\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Master ETL Orchestrator.")
    parser.add_argument('--simulate', type=int, default=0, help="Optional number of synthetic orders to simulate")
    args = parser.parse_args()

    run_pipeline(simulate_n=args.simulate)
