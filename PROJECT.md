# Project: Brazilian E-Commerce (Olist) Power BI & Multi-Cloud Showcase

## Architecture
- **Tier 1 (OLTP Fact Layer):** Supabase Cloud PostgreSQL (4 fact tables: `fact_orders`, `fact_order_items`, `fact_payments`, `fact_reviews`, 415K+ rows, PgBouncer IPv4 session pooler, RLS enabled).
- **Tier 2 (Analytical Dimension Layer):** Google BigQuery Sandbox (`golden-toolbox-431720-i9.olist_ecommerce`, 4 dimension tables: `dim_customers`, `dim_products`, `dim_sellers`, `dim_date`, 136K+ rows, Apache Arrow streaming).
- **Tier 3 (Governance & Parameter Layer):** Google Sheets Live REST API (`category_translation` 73 rows, `kpi_targets` 5 rows disconnected parameter table).
- **Tier 4 (Semantic Model & Visualization Layer):** Power BI Desktop & Service (`Olist_Dashboard.pbix`, 19 DAX measures in 5 display folders, 3-page interactive report).

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Pre-Push Security Audit & .gitignore | Create robust `.gitignore` excluding `.env`, `docs/gcp_service_account.json`, `venv/`, `.agents/`, temp files | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Sanitized Environment Config | Verify/enhance `.env.example` with clear placeholder keys and zero secrets | M1 | ORIGINAL_REQUEST §R1 |
| 3 | Visual Screenshot Extraction | Extract 3 pristine 4K PNG screenshots from `reports/olist_executive_dashboard.pdf` to `docs/assets/` | M1 | ORIGINAL_REQUEST §R4 |
| 4 | Live Power BI Service Integration | Embed live Power BI Service link prominently in README.md with clear access context | M1 | ORIGINAL_REQUEST §R2 |
| 5 | Executive Deliverables Linking | Link PDF deliverable, PPTX presentation, findings report, and PBIX model | M1 | ORIGINAL_REQUEST §R3, §R4 |
| 6 | Comprehensive Showcase README | Overhaul README with architecture, star schema, 19 DAX library, data dictionary, and insights | M1 | ORIGINAL_REQUEST §R4 |
| 7 | Git Staging & Clean Commit | Initialize git, stage audited files, verify zero secrets tracked, create structured commit | M2 | ORIGINAL_REQUEST §R5 |
| 8 | Push Command & Verification | Deliver exact git command for user push without executing remote push | M2 | ORIGINAL_REQUEST §R5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Showcase & Security Implementation | Implement `.gitignore`, `.env.example`, extract 3 visual screenshots to `docs/assets/`, overhaul `README.md` with live link, architecture, DAX library, and deliverables | Survey Phase | IN_PROGRESS |
| 2 | Verification, Forensic Audit & Git Staging | Verify all files, run forensic security audit, verify zero leaks, stage files, commit locally, document push command | M1 | PLANNED |

## Code Layout
- `README.md`: Root showcase document
- `.gitignore`: Root security exclusions
- `.env.example`: Sanitized configuration template
- `docs/assets/`: Extracted high-fidelity dashboard screenshots
- `reports/olist_executive_dashboard.pdf`: Executive deliverable PDF
- `reports/executive_presentation.pptx`: 10-slide executive deck
- `reports/findings_report.md`: C-Suite advisory findings report
- `Olist_Dashboard.pbix`: Power BI semantic model
- `scripts/`: Ingestion and audit automation scripts

## Interface Contracts
### Extraction Script ↔ Assets Directory
- Source: `reports/olist_executive_dashboard.pdf` (3 pages)
- Target: `docs/assets/dashboard_executive_overview.png`, `docs/assets/dashboard_sales_deep_dive.png`, `docs/assets/dashboard_logistics_sentiment.png`
- Format: 4K / 2x resolution PNG (minimum 144 DPI)

### README.md ↔ Repository Artifacts
- All internal image and deliverable paths must be relative and verifiable
- External link: `https://app.powerbi.com/links/icFXyNaImI?ctid=56c1d497-700b-49cf-8f8d-3dd6b20d522f&pbi_source=linkShare`
