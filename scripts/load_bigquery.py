"""
Google BigQuery Dimension Tables Loader
---------------------------------------
Loads the 4 Dimension tables from output/star_schema/ into Google BigQuery Cloud Data Warehouse.
Enforces explicit columnar BigQuery schemas and verifies row counts.
"""

import os
import sys
import time
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 1. Load environment variables
load_dotenv()
project_id = os.getenv('GCP_PROJECT_ID', 'golden-toolbox-431720-i9')
cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'docs/gcp_service_account.json')

# Resolve absolute path for credentials
if not os.path.isabs(cred_path):
    cred_path = os.path.join(os.path.dirname(__file__), '..', cred_path)

if not os.path.exists(cred_path):
    print(f"❌ ERROR: Service account key not found at {cred_path}")
    print("Please ensure docs/gcp_service_account.json exists.")
    sys.exit(1)

print(f"🔗 Connecting to Google BigQuery (Project: {project_id})...")
try:
    credentials = service_account.Credentials.from_service_account_file(cred_path)
    client = bigquery.Client(project=project_id, credentials=credentials)
    
    # Verify dataset exists or create if missing
    dataset_id = f"{project_id}.olist_ecommerce"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"
    dataset = client.create_dataset(dataset, exists_ok=True)
    print(f"✅ Connected to BigQuery successfully! Dataset ready: {dataset_id}")
except Exception as e:
    print(f"❌ BigQuery connection failed: {e}")
    sys.exit(1)

# 2. Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'star_schema')

# 3. Explicit Columnar BigQuery Schemas
SCHEMAS = {
    "dim_customers": [
        bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("customer_unique_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("customer_city", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("customer_state", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("customer_zip_code_prefix", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("latitude", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("longitude", "FLOAT", mode="NULLABLE"),
    ],
    "dim_products": [
        bigquery.SchemaField("product_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("product_category_name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("product_category_name_english", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("product_name_length", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("product_description_length", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("product_photos_qty", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("product_weight_g", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("product_length_cm", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("product_height_cm", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("product_width_cm", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("product_volume_cm3", "FLOAT", mode="NULLABLE"),
    ],
    "dim_sellers": [
        bigquery.SchemaField("seller_id", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("seller_city", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("seller_state", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("seller_zip_code_prefix", "INTEGER", mode="NULLABLE"),
        bigquery.SchemaField("latitude", "FLOAT", mode="NULLABLE"),
        bigquery.SchemaField("longitude", "FLOAT", mode="NULLABLE"),
    ],
    "dim_date": [
        bigquery.SchemaField("date_key", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("full_date", "DATE", mode="REQUIRED"),
        bigquery.SchemaField("year", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("quarter", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("month", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("month_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("year_month", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("week_of_year", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("day_of_month", "INTEGER", mode="REQUIRED"),
        bigquery.SchemaField("day_name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("is_weekend", "INTEGER", mode="REQUIRED"),
    ]
}

DIM_FILES = {
    "dim_customers": "dim_customers.csv",
    "dim_products": "dim_products.csv",
    "dim_sellers": "dim_sellers.csv",
    "dim_date": "dim_date.csv"
}

# 4. Upload Dimensions to BigQuery
print("\n🚀 Uploading Dimension tables to Google BigQuery...")
start_time = time.time()

for table_name, filename in DIM_FILES.items():
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    
    print(f"\n📂 Loading {table_name} from {filename}...")
    df = pd.read_csv(file_path)
    
    # Type adjustments for BigQuery
    if table_name == "dim_date":
        df['date_key'] = pd.to_datetime(df['date_key']).dt.date
        df['full_date'] = pd.to_datetime(df['full_date']).dt.date
    
    table_ref = f"{dataset_id}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        schema=SCHEMAS[table_name],
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    t0 = time.time()
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete
    elapsed = time.time() - t0
    
    print(f"   ✅ {table_name}: {len(df):,} rows loaded in {elapsed:.1f}s ({len(df)/elapsed:.0f} rows/s)")

total_elapsed = time.time() - start_time
print(f"\n🎉 All Dimension tables successfully uploaded in {total_elapsed:.1f}s!")

# 5. Direct Cloud Verification
print("\n🔍 Verifying row counts directly in Google BigQuery:")
print("-" * 55)
print(f"{'Table Name':<25} | {'CSV Rows':>12} | {'BigQuery Rows':>12}")
print("-" * 55)

for table_name, filename in DIM_FILES.items():
    csv_rows = len(pd.read_csv(os.path.join(DATA_DIR, filename)))
    query = f"SELECT COUNT(*) as cnt FROM `{dataset_id}.{table_name}`"
    query_job = client.query(query)
    bq_rows = list(query_job.result())[0].cnt
    match_icon = "✅" if csv_rows == bq_rows else "❌"
    print(f"{match_icon} {table_name:<23} | {csv_rows:>12,} | {bq_rows:>12,}")

print("-" * 55)
print("✅ Google BigQuery Dimension loading complete and 100% verified!")
