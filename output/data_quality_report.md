# 🛡️ Data Quality & Referential Integrity Audit Report

**Generated:** 2026-11-01 14:21:57  
**Status:** ALL CHECKS PASSED ✅

## Integrity & Validation Summary Table

| Check Type | Relationship / Test | Result | Issue Count |
|---|---|---|---|
| Referential Integrity | `fact_orders.customer_id -> dim_customers` | ✅ PASS | 0 |
| Referential Integrity | `fact_orders.purchase_date_key -> dim_date` | ✅ PASS | 0 |
| Referential Integrity | `fact_order_items.order_id -> fact_orders` | ✅ PASS | 0 |
| Referential Integrity | `fact_order_items.product_id -> dim_products` | ✅ PASS | 0 |
| Referential Integrity | `fact_order_items.seller_id -> dim_sellers` | ✅ PASS | 0 |
| Referential Integrity | `fact_payments.order_id -> fact_orders` | ✅ PASS | 0 |
| Referential Integrity | `fact_reviews.order_id -> fact_orders` | ✅ PASS | 0 |
| Key Uniqueness | `fact_reviews composite PK (review_id, order_id) uniqueness` | ✅ PASS | 0 |
| Range Check | `Price > 0` | ✅ PASS | 0 |
| Range Check | `Review Score between 1 and 5` | ✅ PASS | 0 |
| Range Check | `Payment Value > 0` | ✅ PASS | 0 |
| Domain Check | `Geolocation coordinates within Brazil bounding box` | ✅ PASS | 0 |
| Completeness Check | `Product attributes completeness (specs null count)` | ✅ PASS | 0 |
