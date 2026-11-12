# Olist Brazilian E-Commerce: Enterprise Data Dictionary

This data dictionary documents the dimensional model schemas, column definitions, data types, and primary/foreign key designations across all **10 tables** in the Olist Business Intelligence platform.

---

## 1. Fact Tables (Stored in Supabase Cloud PostgreSQL)

### 1.1 `fact_orders` (Grain: 1 row per order)
Captures the lifecycle, fulfillment status, and SLA delivery timelines for every transaction.

| Column Name | Data Type | Constraint | Description | Example / Range |
|---|---|:---:|---|---|
| `order_id` | VARCHAR(32) | **PK** | Unique 32-character hexadecimal identifier for the order. | `e481f51cbdc54678b7cc...` |
| `customer_id` | VARCHAR(32) | **FK** | Foreign key linking to `dim_customers.customer_id`. | `9ef432eb6251297304e7...` |
| `purchase_date_key` | DATE | **FK** | Calendar date of purchase linking to `dim_date.date_key`. | `2017-10-02` |
| `order_status` | VARCHAR(20) | - | Order lifecycle state. | `delivered`, `shipped`, `canceled` |
| `order_purchase_timestamp` | TIMESTAMP | - | Exact timestamp of initial purchase. | `2017-10-02 10:56:33` |
| `order_approved_at` | TIMESTAMP | - | Timestamp when payment was authorized. | `2017-10-02 11:07:15` |
| `order_delivered_carrier_date` | TIMESTAMP | - | Timestamp when package was handed off to carrier. | `2017-10-04 19:55:00` |
| `order_delivered_customer_date`| TIMESTAMP | - | Timestamp when package was delivered to customer doorstep. | `2017-10-10 21:25:13` |
| `order_estimated_delivery_date`| TIMESTAMP | - | Promised carrier estimated delivery deadline. | `2017-10-18 00:00:00` |
| `delivery_days_actual` | DOUBLE | - | Total elapsed transit duration in days (delivered - purchase). | `8.44` |
| `delivery_days_estimated` | DOUBLE | - | Expected delivery timeline in days (estimated - purchase). | `15.54` |
| `is_late_delivery` | DOUBLE | - | Binary SLA breach flag (`1.0` if actual date > estimated date, else `0.0`). | `0.0` or `1.0` |

---

### 1.2 `fact_order_items` (Grain: 1 row per line-item within an order)
Contains line-item purchase economics, unit pricing, freight charges, and catalog foreign keys.

| Column Name | Data Type | Constraint | Description | Example / Range |
|---|---|:---:|---|---|
| `order_id` | VARCHAR(32) | **Composite PK, FK** | Foreign key linking to `fact_orders.order_id`. | `00010242fe8c5a6d1b...` |
| `order_item_id` | INT | **Composite PK** | Sequential item index within the order (1, 2, 3...). | `1` |
| `product_id` | VARCHAR(32) | **FK** | Foreign key linking to `dim_products.product_id`. | `4244733e06e7ecb497...` |
| `seller_id` | VARCHAR(32) | **FK** | Foreign key linking to `dim_sellers.seller_id`. | `48436dade18ac8b2bc...` |
| `purchase_date_key` | DATE | **FK** | Calendar date linking to `dim_date.date_key`. | `2017-09-13` |
| `price` | NUMERIC(10, 2) | - | Item unit purchase price in Brazilian Reais (R$). | `58.90` |
| `freight_value` | NUMERIC(10, 2) | - | Shipping and handling freight charge for the item. | `13.29` |
| `total_value` | NUMERIC(10, 2) | - | Additive item total (`price + freight_value`). | `72.19` |
| `freight_to_price_ratio` | DOUBLE | - | Shipping burden ratio (`freight_value / price`). | `0.2256` (22.6%) |

---

### 1.3 `fact_payments` (Grain: 1 row per payment installment / tender)
Preserves payment rails, installment schedules, and multi-tender transactions.

| Column Name | Data Type | Constraint | Description | Example / Range |
|---|---|:---:|---|---|
| `order_id` | VARCHAR(32) | **Composite PK, FK** | Foreign key linking to `fact_orders.order_id`. | `b81ef226f3fe1789b1...` |
| `payment_sequential` | INT | **Composite PK** | Sequence number of payment tender (1, 2...). | `1` |
| `payment_type` | VARCHAR(20) | - | Payment instrument rail. | `credit_card`, `boleto`, `voucher`, `debit_card` |
| `payment_installments` | INT | - | Number of installment billing cycles chosen. | `1` to `24` |
| `payment_value` | NUMERIC(10, 2) | - | Transaction amount charged to this tender. | `99.33` |

---

### 1.4 `fact_reviews` (Grain: 1 row per customer review interaction)
Contains customer satisfaction scores and review timestamps.

| Column Name | Data Type | Constraint | Description | Example / Range |
|---|---|:---:|---|---|
| `review_id` | VARCHAR(32) | **Composite PK** | Unique identifier for customer review event. | `7bc2406110b926393a...` |
| `order_id` | VARCHAR(32) | **Composite PK, FK** | Foreign key linking to `fact_orders.order_id`. | `73fc7af87114b39712...` |
| `review_score` | INT | - | Customer satisfaction score on 1 to 5 discrete scale. | `1`, `2`, `3`, `4`, `5` |
| `review_creation_date` | TIMESTAMP | - | Timestamp when review survey was sent to customer. | `2018-01-18 00:00:00` |
| `review_answer_timestamp` | TIMESTAMP | - | Timestamp when customer submitted feedback. | `2018-01-18 21:46:00` |

---

## 2. Dimension Tables (Stored in Google BigQuery Sandbox)

### 2.1 `dim_customers` (Grain: 1 row per unique customer order address)
Contains customer geographic attributes and unique human buyer identifiers.

| Column Name | Data Type | Constraint | Description |
|---|---|:---:|---|
| `customer_id` | STRING | **PK** | Unique identifier per order-customer instance. |
| `customer_unique_id` | STRING | - | True deduplicated human identifier (enables repeat purchase tracking). |
| `customer_city` | STRING | - | Cleaned, accent-normalized municipality name. |
| `customer_state` | STRING | - | Brazilian state 2-letter abbreviation (`SP`, `RJ`, `MG`...). |
| `customer_zip_code_prefix`| INT64 | - | 5-digit postal zip code prefix. |
| `latitude` | FLOAT64 | - | Median geographic latitude within Brazil (-34.0 to 5.5). |
| `longitude` | FLOAT64 | - | Median geographic longitude within Brazil (-74.0 to -34.0). |

---

### 2.2 `dim_products` (Grain: 1 row per unique catalog product)
Contains product physical specifications, categories, and volumetric measurements.

| Column Name | Data Type | Constraint | Description |
|---|---|:---:|---|
| `product_id` | STRING | **PK** | Unique 32-character product identifier. |
| `product_category_name` | STRING | - | Category classification in Portuguese. |
| `product_category_name_english` | STRING | - | English translation joined from lookup. |
| `product_name_length` | INT64 | - | Character count of product title. |
| `product_description_length`| INT64 | - | Character count of product description. |
| `product_photos_qty` | INT64 | - | Number of product catalog photos published. |
| `product_weight_g` | FLOAT64 | - | Product shipping weight in grams (g). |
| `product_length_cm` | FLOAT64 | - | Package physical length in centimeters. |
| `product_height_cm` | FLOAT64 | - | Package physical height in centimeters. |
| `product_width_cm` | FLOAT64 | - | Package physical width in centimeters. |
| `product_volume_cm3` | FLOAT64 | - | Volumetric cubic volume ($L \times H \times W$). |

---

### 2.3 `dim_sellers` (Grain: 1 row per merchant)
Contains seller location and postal mapping.

| Column Name | Data Type | Constraint | Description |
|---|---|:---:|---|
| `seller_id` | STRING | **PK** | Unique 32-character merchant identifier. |
| `seller_city` | STRING | - | Cleaned, accent-normalized city. |
| `seller_state` | STRING | - | State 2-letter postal code. |
| `seller_zip_code_prefix` | INT64 | - | 5-digit postal prefix. |
| `latitude` | FLOAT64 | - | Median merchant latitude. |
| `longitude` | FLOAT64 | - | Median merchant longitude. |

---

### 2.4 `dim_date` (Grain: 1 row per calendar day)
Enterprise calendar table powering all time intelligence DAX functions.

| Column Name | Data Type | Constraint | Description | Range |
|---|---|:---:|---|---|
| `date_key` | DATE | **PK** | Calendar date key (`YYYY-MM-DD`). | `2016-09-04` to `2018-11-12` |
| `full_date` | DATE | - | Full calendar date representation. | `2016-09-04` to `2018-11-12` |
| `year` | INT64 | - | Calendar Year. | `2016`, `2017`, `2018` |
| `quarter` | INT64 | - | Calendar Quarter. | `1`, `2`, `3`, `4` |
| `month` | INT64 | - | Calendar Month number. | `1` through `12` |
| `month_name` | STRING | - | Month name (sorted by `month`). | `January` through `December` |
| `year_month` | STRING | - | Chronological sort string. | `2017-01` |
| `week_of_year` | INT64 | - | ISO Week of year. | `1` through `53` |
| `day_of_month` | INT64 | - | Day of month. | `1` through `31` |
| `day_name` | STRING | - | Day of week name. | `Monday` through `Sunday` |
| `is_weekend` | INT64 | - | Binary weekend indicator. | `0` = Weekday, `1` = Weekend |

---

## 3. Lookup & Reference Tables (Google Sheets Web REST API)

### 3.1 `category_translation` (73 rows)
Maps Portuguese product category strings to standard international English nomenclature.

### 3.2 `kpi_targets` (5 rows)
Disconnected corporate benchmark parameter table defining executive targets (On-Time SLA 95.0%, Freight Ratio <20%, Review Score >4.0).
