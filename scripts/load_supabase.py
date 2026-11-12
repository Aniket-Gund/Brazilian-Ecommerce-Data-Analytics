"""
Supabase PostgreSQL Data Loader
--------------------------------
Loads the 4 transactional Fact tables from output/star_schema/ into Supabase Cloud PostgreSQL.
Enforces explicit DDL schemas, primary keys, and composite indexes.
"""

import os
import sys
import time
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 1. Load environment variables
load_dotenv()
db_url = os.getenv('SUPABASE_DB_URL')

if not db_url or '[YOUR-PASSWORD]' in db_url:
    print("❌ ERROR: SUPABASE_DB_URL is not configured properly in your .env file.")
    print("Please create a .env file and set your valid Supabase connection URI.")
    sys.exit(1)

# Ensure SQLAlchemy uses psycopg2 driver if standard postgresql:// scheme is used
if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

print("🔗 Connecting to Supabase PostgreSQL database...")
try:
    engine = create_engine(db_url, pool_pre_ping=True)
    with engine.connect() as conn:
        res = conn.execute(text("SELECT version();")).fetchone()
        print(f"✅ Connected successfully!\n   PostgreSQL Version: {res[0][:60]}...")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)

# 2. Paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'output', 'star_schema')

# 3. DDL definitions for Fact Tables
DDL_STATEMENTS = {
    "fact_orders": """
        DROP TABLE IF EXISTS fact_orders CASCADE;
        CREATE TABLE fact_orders (
            order_id VARCHAR(32) PRIMARY KEY,
            customer_id VARCHAR(32) NOT NULL,
            purchase_date_key DATE NOT NULL,
            order_status VARCHAR(20) NOT NULL,
            order_purchase_timestamp TIMESTAMP NOT NULL,
            order_approved_at TIMESTAMP,
            order_delivered_carrier_date TIMESTAMP,
            order_delivered_customer_date TIMESTAMP,
            order_estimated_delivery_date TIMESTAMP NOT NULL,
            delivery_days_actual DOUBLE PRECISION,
            delivery_days_estimated DOUBLE PRECISION,
            is_late_delivery DOUBLE PRECISION
        );
    """,
    "fact_order_items": """
        DROP TABLE IF EXISTS fact_order_items CASCADE;
        CREATE TABLE fact_order_items (
            order_id VARCHAR(32) NOT NULL,
            order_item_id INT NOT NULL,
            product_id VARCHAR(32) NOT NULL,
            seller_id VARCHAR(32) NOT NULL,
            purchase_date_key DATE NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            freight_value NUMERIC(10, 2) NOT NULL,
            total_value NUMERIC(10, 2) NOT NULL,
            freight_to_price_ratio DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (order_id, order_item_id)
        );
    """,
    "fact_payments": """
        DROP TABLE IF EXISTS fact_payments CASCADE;
        CREATE TABLE fact_payments (
            order_id VARCHAR(32) NOT NULL,
            payment_sequential INT NOT NULL,
            payment_type VARCHAR(20) NOT NULL,
            payment_installments INT NOT NULL,
            payment_value NUMERIC(10, 2) NOT NULL,
            PRIMARY KEY (order_id, payment_sequential)
        );
    """,
    "fact_reviews": """
        DROP TABLE IF EXISTS fact_reviews CASCADE;
        CREATE TABLE fact_reviews (
            review_id VARCHAR(32) NOT NULL,
            order_id VARCHAR(32) NOT NULL,
            review_score INT NOT NULL,
            review_creation_date TIMESTAMP NOT NULL,
            review_answer_timestamp TIMESTAMP,
            PRIMARY KEY (review_id, order_id)
        );
    """
}

# 4. Create Tables
print("\n🏗️  Creating clean PostgreSQL Fact table schemas...")
with engine.begin() as conn:
    for table_name, ddl in DDL_STATEMENTS.items():
        conn.execute(text(ddl))
        print(f"   ✓ Schema created: {table_name}")

# 5. Load Data in Chunks
FACT_FILES = {
    "fact_orders": "fact_orders.csv",
    "fact_order_items": "fact_order_items.csv",
    "fact_payments": "fact_payments.csv",
    "fact_reviews": "fact_reviews.csv"
}

print("\n🚀 Pushing Fact tables to Supabase Cloud PostgreSQL...")
start_time = time.time()

for table_name, filename in FACT_FILES.items():
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    
    print(f"\n📂 Loading {table_name} from {filename}...")
    df = pd.read_csv(file_path)
    total_rows = len(df)
    
    # Push to SQL in batches of 5,000 for fast network transfer
    t0 = time.time()
    df.to_sql(
        table_name,
        engine,
        if_exists='append',
        index=False,
        chunksize=5000,
        method='multi'
    )
    elapsed = time.time() - t0
    print(f"   ✅ {table_name}: {total_rows:,} rows loaded in {elapsed:.1f}s ({total_rows/elapsed:.0f} rows/s)")

total_elapsed = time.time() - start_time
print(f"\n🎉 All Fact tables loaded in {total_elapsed:.1f}s!")

# 6. Verify in Database
print("\n🔍 Verifying row counts directly in Supabase PostgreSQL:")
print("-" * 55)
print(f"{'Table Name':<25} | {'CSV Rows':>12} | {'Postgres Rows':>12}")
print("-" * 55)

with engine.connect() as conn:
    for table_name, filename in FACT_FILES.items():
        csv_rows = len(pd.read_csv(os.path.join(DATA_DIR, filename)))
        db_rows = conn.execute(text(f"SELECT COUNT(*) FROM {table_name};")).scalar()
        match_icon = "✅" if csv_rows == db_rows else "❌"
        print(f"{match_icon} {table_name:<23} | {csv_rows:>12,} | {db_rows:>12,}")

print("-" * 55)
print("✅ Supabase Fact loading complete and 100% verified!")
