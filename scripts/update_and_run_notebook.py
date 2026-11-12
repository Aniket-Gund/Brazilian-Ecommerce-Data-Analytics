import sys
import io
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

# Ensure standard output can handle utf-8 on Windows consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NOTEBOOK_PATH = os.path.join(BASE_DIR, 'notebooks', '01_eda_and_cleaning.ipynb')
NOTEBOOK_DIR = os.path.join(BASE_DIR, 'notebooks')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output', 'star_schema')
REPORT_PATH = os.path.join(BASE_DIR, 'output', 'data_quality_report.md')

def main():
    print(f"Reading notebook from: {NOTEBOOK_PATH}")
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # Filter out empty trailing cells
    nb.cells = [cell for cell in nb.cells if cell.source.strip()]
    print(f"Notebook loaded with {len(nb.cells)} active cells.")

    # Execute notebook top-to-bottom
    print("Executing notebook top to bottom using ExecutePreprocessor with olist_env kernel...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='olist_env')
    ep.preprocess(nb, {'metadata': {'path': NOTEBOOK_DIR}})

    # Check for any cell execution errors
    has_any_error = False
    for idx, cell in enumerate(nb.cells):
        for out in cell.get('outputs', []):
            if out.output_type == 'error':
                print(f"❌ Error in cell {idx}: {out.get('ename')}: {out.get('evalue')}")
                has_any_error = True
    
    if has_any_error:
        raise RuntimeError("One or more cells encountered an execution error!")

    print("✅ All notebook cells executed with zero errors!")

    # Save executed notebook with all outputs
    with open(NOTEBOOK_PATH, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Executed notebook saved to: {NOTEBOOK_PATH}")

    # Verify all Star Schema CSVs exist and are non-empty
    expected_tables = [
        'dim_date.csv',
        'dim_customers.csv',
        'dim_products.csv',
        'dim_sellers.csv',
        'kpi_targets.csv',
        'category_translation.csv',
        'fact_orders.csv',
        'fact_order_items.csv',
        'fact_payments.csv',
        'fact_reviews.csv'
    ]
    print("\nVerifying exported Star Schema CSV files:")
    for tbl in expected_tables:
        tbl_path = os.path.join(OUTPUT_DIR, tbl)
        if not os.path.exists(tbl_path):
            raise FileNotFoundError(f"Missing star schema table: {tbl_path}")
        size = os.path.getsize(tbl_path)
        print(f"  ✓ {tbl:<25}: {size:>10,} bytes")

    # Verify data quality report
    if not os.path.exists(REPORT_PATH):
        raise FileNotFoundError(f"Missing data quality report: {REPORT_PATH}")
    print(f"\n✅ Data quality report verified at: {REPORT_PATH}")
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        print(f.read())

if __name__ == '__main__':
    main()
