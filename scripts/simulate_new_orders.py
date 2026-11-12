"""
Olist E-Commerce: Order Generation & Ingestion Engine (Step 8)
---------------------------------------------------------------
Simulates realistic, transaction-consistent incoming orders and 
streams them directly into Supabase Cloud PostgreSQL.

Maintains:
1. 100% Kimball dimensional referential integrity (valid foreign keys to BigQuery dimensions).
2. True business logic correlation (delivery transit duration directly drives review scores).
3. Chronological timeline continuity (attaches to Sept/Oct 2018 within dim_date coverage).
4. Atomic database transaction with before/after executive telemetry.
"""

import os
import sys
import uuid
import random
import argparse
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 1. Load Environment & Setup Database Connection
load_dotenv()
db_url = os.getenv('SUPABASE_DB_URL')
if not db_url:
    print("❌ ERROR: SUPABASE_DB_URL is missing in your .env file.")
    sys.exit(1)

if db_url.startswith('postgresql://'):
    db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)

engine = create_engine(db_url, pool_pre_ping=True)

# 2. Paths to Reference Dimensions
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'output', 'star_schema')

def load_dimension_samples():
    """Loads valid keys from dimension tables to guarantee 100% referential integrity."""
    print("📂 Loading dimension keys from star schema for referential integrity...")
    customers_df = pd.read_csv(os.path.join(DATA_DIR, 'dim_customers.csv'), usecols=['customer_id'])
    products_df = pd.read_csv(os.path.join(DATA_DIR, 'dim_products.csv'), usecols=['product_id'])
    sellers_df = pd.read_csv(os.path.join(DATA_DIR, 'dim_sellers.csv'), usecols=['seller_id'])
    dates_df = pd.read_csv(os.path.join(DATA_DIR, 'dim_date.csv'), usecols=['date_key'])
    
    return {
        'customer_ids': customers_df['customer_id'].dropna().values,
        'product_ids': products_df['product_id'].dropna().values,
        'seller_ids': sellers_df['seller_id'].dropna().values,
        'valid_dates': set(dates_df['date_key'].values)
    }

def generate_synthetic_orders(num_orders=500, dims=None):
    """Generates synthetic, correlated transactional records across all 4 Fact tables."""
    print(f"\n⚙️  Synthesizing {num_orders:,} realistic orders with correlated business logic...")
    random.seed(42)
    np.random.seed(42)

    orders_list = []
    items_list = []
    payments_list = []
    reviews_list = []

    # Simulation date window: Sept 4, 2018 to Oct 15, 2018 (seamless continuity after dataset cutoff)
    start_sim_date = datetime(2018, 9, 4, 8, 0, 0)
    end_sim_date = datetime(2018, 10, 15, 22, 0, 0)
    total_seconds = int((end_sim_date - start_sim_date).total_seconds())

    for _ in range(num_orders):
        order_id = uuid.uuid4().hex
        customer_id = str(np.random.choice(dims['customer_ids']))
        
        # Timestamp logic
        random_sec = random.randint(0, total_seconds)
        purchase_ts = start_sim_date + timedelta(seconds=random_sec)
        purchase_date_key = purchase_ts.strftime('%Y-%m-%d')
        
        # Ensure date key exists in dim_date
        if purchase_date_key not in dims['valid_dates']:
            purchase_date_key = '2018-09-15'
            purchase_ts = datetime(2018, 9, 15, 12, 0, 0)

        approved_ts = purchase_ts + timedelta(hours=random.uniform(0.2, 18.0))
        carrier_ts = approved_ts + timedelta(days=random.uniform(1.0, 3.5))

        # 93.5% On-Time SLA distribution matching historical macro metrics
        is_late = np.random.choice([0.0, 1.0], p=[0.935, 0.065])
        estimated_days = random.randint(16, 28)
        estimated_delivery_ts = (purchase_ts + timedelta(days=estimated_days)).replace(hour=0, minute=0, second=0)

        if is_late == 1.0:
            actual_days = estimated_days + random.uniform(2.0, 14.0)
        else:
            actual_days = max(4.0, estimated_days - random.uniform(2.0, 12.0))

        delivered_customer_ts = purchase_ts + timedelta(days=actual_days)
        
        # Order Status: 97.2% delivered, 1.8% shipped, 1.0% canceled
        order_status = np.random.choice(['delivered', 'shipped', 'canceled'], p=[0.972, 0.018, 0.010])
        if order_status == 'shipped':
            delivered_customer_ts = None
            actual_days = None
            is_late = 0.0
        elif order_status == 'canceled':
            carrier_ts = None
            delivered_customer_ts = None
            actual_days = None
            is_late = 0.0

        orders_list.append({
            'order_id': order_id,
            'customer_id': customer_id,
            'purchase_date_key': purchase_date_key,
            'order_status': order_status,
            'order_purchase_timestamp': purchase_ts,
            'order_approved_at': approved_ts,
            'order_delivered_carrier_date': carrier_ts,
            'order_delivered_customer_date': delivered_customer_ts,
            'order_estimated_delivery_date': estimated_delivery_ts,
            'delivery_days_actual': actual_days,
            'delivery_days_estimated': float(estimated_days),
            'is_late_delivery': is_late
        })

        # Items logic (1 to 3 items per order, typical e-commerce basket)
        num_items = np.random.choice([1, 2, 3], p=[0.88, 0.09, 0.03])
        order_total_value = 0.0

        for item_idx in range(1, num_items + 1):
            product_id = str(np.random.choice(dims['product_ids']))
            seller_id = str(np.random.choice(dims['seller_ids']))
            
            # Realistic price ($25 to $320) and freight ($12 to $38)
            price = round(float(np.random.exponential(scale=75.0) + 19.90), 2)
            freight = round(float(np.random.uniform(11.50, 32.00)), 2)
            total_item_val = round(price + freight, 2)
            order_total_value += total_item_val

            items_list.append({
                'order_id': order_id,
                'order_item_id': item_idx,
                'product_id': product_id,
                'seller_id': seller_id,
                'purchase_date_key': purchase_date_key,
                'price': price,
                'freight_value': freight,
                'total_value': total_item_val,
                'freight_to_price_ratio': round(freight / price, 4)
            })

        order_total_value = round(order_total_value, 2)

        # Payments logic (Credit Card ~75%, Boleto ~18%, Voucher ~4%, Debit Card ~3%)
        payment_type = np.random.choice(['credit_card', 'boleto', 'voucher', 'debit_card'], p=[0.75, 0.18, 0.04, 0.03])
        installments = random.randint(1, 8) if payment_type == 'credit_card' else 1

        payments_list.append({
            'order_id': order_id,
            'payment_sequential': 1,
            'payment_type': payment_type,
            'payment_installments': installments,
            'payment_value': order_total_value
        })

        # Reviews logic (Correlated with delivery performance!)
        if order_status == 'delivered':
            # Late orders strongly trigger 1-star reviews (reproducing our Page 3 finding)
            if is_late == 1.0 or (actual_days and actual_days > 20.0):
                review_score = int(np.random.choice([1, 2, 3], p=[0.72, 0.18, 0.10]))
            else:
                review_score = int(np.random.choice([5, 4, 3, 2, 1], p=[0.68, 0.20, 0.07, 0.03, 0.02]))
            
            review_create_ts = delivered_customer_ts + timedelta(days=random.uniform(0.5, 3.0))
            review_answer_ts = review_create_ts + timedelta(hours=random.uniform(2.0, 48.0))

            reviews_list.append({
                'review_id': uuid.uuid4().hex,
                'order_id': order_id,
                'review_score': review_score,
                'review_creation_date': review_create_ts,
                'review_answer_timestamp': review_answer_ts
            })

    df_orders = pd.DataFrame(orders_list)
    df_items = pd.DataFrame(items_list)
    df_payments = pd.DataFrame(payments_list)
    df_reviews = pd.DataFrame(reviews_list)

    return df_orders, df_items, df_payments, df_reviews

def stream_to_supabase(df_orders, df_items, df_payments, df_reviews):
    """Pushes generated batches to Supabase within an atomic transaction."""
    print("\n🔗 Connecting to Supabase Cloud PostgreSQL for batch ingestion...")
    
    with engine.begin() as conn:
        # Pre-ingestion counts
        pre_orders = conn.execute(text("SELECT count(*) FROM fact_orders")).scalar()
        pre_gmv = conn.execute(text("SELECT COALESCE(SUM(total_value), 0) FROM fact_order_items")).scalar()
        
        print(f"   📊 Current Supabase Fact Orders: {pre_orders:,}")
        print(f"   💰 Current Supabase Fact GMV:    ${pre_gmv:,.2f}")

        # Ingestion
        print(f"\n📥 Appending {len(df_orders):,} rows to fact_orders...")
        df_orders.to_sql('fact_orders', conn, if_exists='append', index=False)
        
        print(f"📥 Appending {len(df_items):,} rows to fact_order_items...")
        df_items.to_sql('fact_order_items', conn, if_exists='append', index=False)
        
        print(f"📥 Appending {len(df_payments):,} rows to fact_payments...")
        df_payments.to_sql('fact_payments', conn, if_exists='append', index=False)
        
        print(f"📥 Appending {len(df_reviews):,} rows to fact_reviews...")
        df_reviews.to_sql('fact_reviews', conn, if_exists='append', index=False)

        # Post-ingestion counts
        post_orders = conn.execute(text("SELECT count(*) FROM fact_orders")).scalar()
        post_gmv = conn.execute(text("SELECT COALESCE(SUM(total_value), 0) FROM fact_order_items")).scalar()

    added_orders = post_orders - pre_orders
    added_gmv = float(post_gmv) - float(pre_gmv)

    print("\n" + "="*65)
    print("🎉 INGESTION PIPELINE EXECUTION SUCCESSFUL (100% COMMITTED)")
    print("="*65)
    print(f"📦 Total Orders Before:  {pre_orders:,}")
    print(f"➕ Orders Injected:      +{added_orders:,}")
    print(f"📦 Total Orders After:   {post_orders:,}")
    print("-" * 65)
    print(f"💵 Total GMV Before:     ${float(pre_gmv):,.2f}")
    print(f"➕ Incremental GMV:      +${added_gmv:,.2f}")
    print(f"💵 Total GMV After:      ${float(post_gmv):,.2f}")
    print("="*65)
    print("\n👉 NEXT STEP: Open Power BI Desktop and click the 'Refresh' button")
    print("   on the Home ribbon to observe your dashboard absorb the new stream!\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simulate and ingest synthetic orders into Supabase.")
    parser.add_argument('--orders', type=int, default=500, help="Number of synthetic orders to generate (default: 500)")
    args = parser.parse_args()

    dims = load_dimension_samples()
    df_orders, df_items, df_payments, df_reviews = generate_synthetic_orders(num_orders=args.orders, dims=dims)
    stream_to_supabase(df_orders, df_items, df_payments, df_reviews)
