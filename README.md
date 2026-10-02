# Meesho Reseller Growth & Alert Monitoring Pipeline

A deterministic, end-to-end data analytics pipeline for monitoring reseller performance across **categories**, **regions**, and **individual resellers**.

The project simulates a Meesho reseller monitoring workflow in which business and category managers need to identify significant category movements, inactive resellers, and regional performance changes from monthly order data.

The pipeline is intentionally **deterministic and rule-based**. It does not use an LLM or AI-generated numbers:

| Layer | Responsibility |
| --- | --- |
| SQL | Calculates business facts |
| Python rules | Makes business decisions |
| Templates | Communicate verified results |
| Orchestrator | Controls the workflow |

> Every number in a report must come from a verified SQL/Python result. The reporting layer never invents a number.

---

## Table of Contents

1. [Project Objective](#1-project-objective)
2. [Project Status](#2-project-status)
3. [Technology Stack](#3-technology-stack)
4. [Repository Structure](#4-repository-structure)
5. [Getting Started](#5-getting-started)
6. [Dataset Generation](#6-dataset-generation)
7. [Intentional Business Patterns](#7-intentional-business-patterns)
8. [Data Validation](#8-data-validation)
9. [Database](#9-database)
10. [SQL Analytics Layer](#10-sql-analytics-layer)
11. [Python Rules Engine](#11-python-rules-engine)
12. [Current Rule Results](#12-current-rule-results)
13. [Design Principles](#13-design-principles)
14. [Roadmap](#14-roadmap)
15. [Rules for Contributors](#15-rules-for-contributors)
16. [Target Architecture](#16-target-architecture)
17. [Definition of Done](#17-definition-of-done)

---

## 1. Project Objective

Build a small but complete data-driven monitoring system that answers four business questions:

1. **Which categories changed enough to matter?**
2. **Which resellers are inactive?**
3. **Which regions are contributing, and how are they changing?**
4. **How can these findings be turned into a reliable stakeholder report without inventing numbers?**

Pipeline flow:

```text
Synthetic Reseller + Order Data
            |
            v
      Data Validation
            |
            v
       SQLite Database
            |
            v
       SQL Analytics
            |
            v
      Python Rule Engine
            |
            v
          Alerts
            |
            v
   Deterministic Reporting
            |
            v
     Output Validation
            |
            v
       Human Review
```

---

## 2. Project Status

| Component | Status |
| --- | --- |
| Synthetic dataset generation | Done |
| CSV generation | Done |
| SQLite database creation | Done |
| Data validation | Done |
| Category analytics | Done |
| Reseller activity analytics | Done |
| Regional analytics | Done |
| Category month-over-month analysis | Done |
| Category alert rules | Done |
| Inactive reseller rule | Done |
| Manual execution of analytics and rules | Done |
| Automated pytest test suite | Planned |
| Regional month-over-month analysis | Planned |
| Combined alert output | Planned |
| Alert persistence | Planned |
| Deterministic report generator | Planned |
| Report validation | Planned |
| Agent / orchestrator specification | Planned |
| Mock agent runner | Planned |
| Single end-to-end entry point | Planned |
| Final project demonstration | Planned |

---

## 3. Technology Stack

- **Python 3**
- **pandas**: DataFrames for query results and validation
- **SQLite**: local, file-based database
- **SQL**: all business metrics, including `LAG()` window functions
- **CSV**: raw data export
- **pytest**: test framework (test suite in progress)

Standard-library modules used: `sqlite3`, `csv`, `random`, `os`, `datetime`.

No external LLM or API is required.

---

## 4. Repository Structure

### Current

```text
Project_kabilan/
│
├── data/
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── src/
│   ├── generate_dataset.py      # Builds CSVs + SQLite DB (seed 42)
│   ├── validate_dataset.py      # Data quality checks
│   ├── analytics.py             # Runs SQL files, returns DataFrames
│   ├── rules.py                 # Business rules -> alerts
│   ├── test_analytics.py        # Manual script: prints analytics
│   ├── test_rules.py            # Manual script: prints alerts
│   └── sql/
│       ├── 01_category_metrics.sql
│       ├── 02_reseller_activity.sql
│       ├── 03_region_metrics.sql
│       └── 04_category_mom.sql
│
├── requirements.txt
├── .gitignore
└── README.md
```

### Planned additions

```text
├── src/sql/05_region_mom.sql
├── tests/
│   ├── test_analytics.py
│   ├── test_rules.py
│   └── ...
├── reporting/
│   ├── report_generator.py
│   └── report_validator.py
├── agent/
│   ├── specification.md
│   └── mock_runner.py
├── outputs/
│   ├── alerts.json
│   ├── monthly_report.txt
│   └── regional_summary.csv
└── run_pipeline.py
```

---

## 5. Getting Started

### Installation (Windows PowerShell)

```powershell
git clone <repository-url>
cd <repository>

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

On macOS/Linux, activate with `source .venv/bin/activate`.

### Running the current pipeline

Run the steps in this order from the project root:

```powershell
python src\generate_dataset.py    # 1. Create CSVs and SQLite DB
python src\validate_dataset.py    # 2. Validate the data
python src\test_analytics.py      # 3. Print SQL analytics results
python src\test_rules.py          # 4. Print generated alerts
```

When complete, the whole workflow will run with a single command:

```powershell
python run_pipeline.py
pytest
```

---

## 6. Dataset Generation

**File:** `src/generate_dataset.py`

The generator creates a reproducible synthetic dataset using a fixed seed:

```python
rng = random.Random(42)
```

The same data is produced on every run.

### Resellers

24 resellers (`R001` to `R024`), six per region:

| Region | Cities |
| --- | --- |
| North | Delhi, Jaipur, Lucknow |
| South | Bengaluru, Chennai, Hyderabad |
| East | Kolkata, Patna, Bhubaneswar |
| West | Mumbai, Pune, Ahmedabad |

### Orders

900 orders, 300 per month (April, May, June 2026).

**Categories:** Ethnic Wear, Western Wear, Kids Wear, Home & Kitchen, Beauty & Personal Care. Each category has six products and its own price range.

**Quantity:** 1 to 5 units per order.

**Status probabilities:**

| Status | Probability |
| --- | --- |
| Delivered | 70% |
| Returned | 15% |
| Cancelled | 10% |
| Pending | 5% |

---

## 7. Intentional Business Patterns

The dataset is not completely random. Patterns were deliberately introduced so the monitoring system has meaningful events to detect.

**Ethnic Wear** (share of monthly orders): a large spike followed by a decline.

| April | May | June |
| --- | --- | --- |
| 20% | 34% | 18% |

**Home & Kitchen** (share of monthly orders): a May dip followed by a June recovery.

| April | May | June |
| --- | --- | --- |
| 20% | 14% | 22% |

**Inactive reseller:** `R024` never receives any orders. This gives the inactivity rule an explicit edge case.

---

## 8. Data Validation

**File:** `src/validate_dataset.py`

Checks performed:

- Reseller and order row counts
- Missing values
- Duplicate IDs
- Monthly order counts
- Order status distribution
- Foreign-key consistency (every order references a real reseller)
- Resellers without orders
- Database row counts match the CSV files

Expected results (all checks currently pass):

| Check | Expected |
| --- | --- |
| Resellers | 24 |
| Orders | 900 |
| Orders per month | 300 / 300 / 300 |
| Delivered | 644 |
| Returned | 118 |
| Cancelled | 93 |
| Pending | 45 |
| Missing values | 0 |
| Duplicate IDs | 0 |
| Invalid reseller references | 0 |
| Resellers with no orders | `R024` only |

---

## 9. Database

**File:** `data/meesho_reseller.db`

| Table | Primary key | Notes |
| --- | --- | --- |
| `resellers` | `reseller_id` | Name, city, region, join date |
| `orders` | `order_id` | Foreign key `reseller_id` references `resellers` |

The analytics layer queries this database, not the CSV files.

---

## 10. SQL Analytics Layer

SQL queries live in `src/sql/`, separate from Python, so the business calculations stay readable and easy to change. `src/analytics.py` provides a `run_query()` helper that executes a `.sql` file and returns a pandas DataFrame.

All metrics count **only** orders where `status = 'Delivered'`.

**GMV = `quantity × unit_price`**

| SQL file | Python function | Output columns |
| --- | --- | --- |
| `01_category_metrics.sql` | `get_category_metrics()` | month, category, order_count, units_sold, gmv |
| `02_reseller_activity.sql` | `get_reseller_activity()` | reseller_id, reseller_name, region, city, delivered_orders, gmv |
| `03_region_metrics.sql` | `get_region_metrics()` | region, reseller_count, delivered_orders, gmv |
| `04_category_mom.sql` | `get_category_mom()` | category, month, current_gmv, previous_gmv, change_pct, change_amount |

### Notes

- **Reseller activity** uses a `LEFT JOIN` on purpose, so resellers with zero orders stay visible. This is how `R024` is detected.
- **Category MoM** uses the `LAG()` window function to compare each category with the previous month.

### Current regional GMV

| Region | GMV |
| --- | ---: |
| South | ₹743,211 |
| East | ₹742,880 |
| North | ₹664,797 |
| West | ₹560,339 |

---

## 11. Python Rules Engine

**File:** `src/rules.py`

SQL calculates the facts. Python decides whether those facts meet a business rule. This separation is intentional.

### Significant category change

```python
PERCENT_THRESHOLD = 15.0
GMV_THRESHOLD = 30000.0
```

A category change is significant only when **both** conditions hold:

```text
|change_pct|    >= 15%
AND
|change_amount| >= ₹30,000
```

Requiring both prevents alerts caused by large percentages on small absolute amounts.

| Direction | Alert type |
| --- | --- |
| Positive | `CATEGORY_GROWTH` |
| Negative | `CATEGORY_DECLINE` |

### Inactive reseller

A reseller is inactive when `delivered_orders == 0`.

Alert type: `RESELLER_INACTIVE`

---

## 12. Current Rule Results

The current dataset produces **8 alerts**: 7 category alerts and 1 inactive reseller alert.

### Category alerts

| Month | Category | Change % | Change (₹) | Type |
| --- | --- | ---: | ---: | --- |
| May | Ethnic Wear | +42.23% | +92,270 | Growth |
| May | Home & Kitchen | −18.84% | −36,275 | Decline |
| June | Beauty & Personal Care | +42.65% | +46,509 | Growth |
| June | Ethnic Wear | −46.68% | −145,052 | Decline |
| June | Home & Kitchen | +96.31% | +150,471 | Growth |
| June | Kids Wear | +33.47% | +39,323 | Growth |
| June | Western Wear | −15.04% | −32,489 | Decline |

### Inactive reseller alert

| Reseller | Region | City | Delivered orders | GMV |
| --- | --- | --- | ---: | ---: |
| R024 | West | Ahmedabad | 0 | ₹0 |

### Example alert object

```json
{
    "alert_type": "CATEGORY_GROWTH",
    "category": "Ethnic Wear",
    "month": "May",
    "current_gmv": 310767.0,
    "previous_gmv": 218497.0,
    "change_pct": 42.23,
    "change_amount": 92270.0
}
```

---

## 13. Design Principles

1. **No LLM in the core pipeline.** Results must be reproducible and auditable.
2. **SQL is the single source of facts.** Metrics are calculated once, in SQL.
3. **Rules are explicit.** Thresholds are named constants, not magic numbers.
4. **Reporting only communicates.** The report generator must not recalculate metrics such as `(current - previous) / previous`. It formats values already produced by the SQL/rules layer.
5. **Fail loudly.** The reporting layer should fail rather than silently produce an incorrect report.
6. **Nothing is hidden.** Edge cases such as zero-order resellers must stay visible.

---

## 14. Roadmap

Complete the remaining work **in this order**. Proper tests come first, so later stages have a stable contract to depend on.

### Step 1: Convert print scripts into real pytest tests

Create a `tests/` folder with real `def test_...()` functions and `assert` statements, replacing the print-based scripts in `src/`.

Minimum tests:

- 24 resellers exist
- 900 orders exist
- 300 orders exist for each month
- 644 delivered orders
- `R024` has zero delivered orders
- 7 category alerts are generated
- 1 inactive reseller alert is generated
- `R024` is the inactive reseller

Target: `pytest` passes with all tests green.

### Step 2: Regional month-over-month analysis

Create `src/sql/05_region_mom.sql` using `LAG()`, mirroring the category MoM query. Output columns: `region, month, current_gmv, previous_gmv, change_pct, change_amount`.

Add to `analytics.py`:

```python
def get_region_mom():
    return run_query("05_region_mom.sql")
```

Add tests for the new query.

### Step 3: Combined alert engine

Combine all alert sources into one collection:

```python
alerts = []
alerts.extend(find_category_alerts(category_df))
alerts.extend(find_inactive_resellers(reseller_df))
alerts.extend(find_region_alerts(region_df))
```

Every alert must share a consistent structure with at least:

```text
alert_type
severity
period
entity
message / data
```

> Do not invent severity rankings without first defining the business rule. If severity is introduced, document exactly how it is calculated.

### Step 4: Persist alerts

Write alerts to `outputs/alerts.json` (or `alerts.csv`). **Persist values exactly as produced by the analytics/rules layer.**

### Step 5: Deterministic report generator

Create `reporting/report_generator.py`. It converts verified alert objects into readable, template-based text. Example:

```text
May Category Update

Ethnic Wear increased by 42.23% in May,
with GMV increasing by ₹92,270 compared with April.

Home & Kitchen declined by 18.84%,
with GMV decreasing by ₹36,275 compared with April.

Inactive Reseller

Reseller R024 in Ahmedabad had no delivered orders
during the monitoring period.
```

No GPT, LLM, OpenAI API, or AI-generated explanations.

### Step 6: Report validation

Create `reporting/report_validator.py` to verify that:

- every alert appears in the report
- category names match
- reseller IDs match
- percentages match
- GMV values match
- no unsupported numeric values appear
- no alert disappears during reporting

### Step 7: Agent specification

Create `agent/specification.md` describing the workflow. The "agent" is an **orchestrator, not an AI model**.

```text
START -> Validate dataset -> Run SQL analytics -> Apply business rules
      -> Generate alerts -> Generate report -> Validate report
      -> Human review -> END
```

Document inputs, outputs, steps, rules, failure conditions, and human review requirements.

### Step 8: Mock agent runner

Create `agent/mock_runner.py`:

```python
def run_pipeline():
    validate_data()
    category_data = get_category_metrics()
    reseller_data = get_reseller_activity()
    region_data = get_region_metrics()

    alerts = create_alerts(category_data, reseller_data, region_data)
    report = generate_report(alerts)
    validate_report(report)

    return report
```

Progress output:

```text
[1/6] Validating dataset...
[2/6] Running SQL analytics...
[3/6] Applying alert rules...
[4/6] Generating report...
[5/6] Validating report...
[6/6] Ready for human review.
```

### Step 9: Single entry point

Create `run_pipeline.py` so the full workflow runs with:

```powershell
python run_pipeline.py
```

```text
Generate data -> Validate -> Analytics -> Rules -> Alerts
             -> Report -> Report validation -> Human review
```

### Step 10: Final tests

| Area | Tests |
| --- | --- |
| Dataset | 24 resellers, 900 orders, 300 orders/month |
| Database | CSV and DB counts match, foreign keys valid |
| Analytics | 644 delivered orders, regional totals, category totals, MoM calculations |
| Rules | 7 category alerts, 1 inactive reseller |
| Reporting | All alerts represented, numbers match source data, no unsupported figures |
| Pipeline | End-to-end execution succeeds |

### Step 11: Example outputs

Commit example outputs so reviewers can see what the system produces:

```text
outputs/
├── alerts.json
├── monthly_report.txt
└── regional_summary.csv
```

### Step 12: Final README update

Update this README with the final architecture, folder structure, example output, testing instructions, design decisions, limitations, and future improvements.

---

## 15. Rules for Contributors

**Do not change the dataset casually.**
The dataset is deliberately designed to exercise the alert rules. Changing the random seed or category weights changes the expected results.

**Do not change thresholds without documenting it.**
If the category rule (`>= 15%` AND `>= ₹30,000`) changes, update `rules.py`, the tests, this README, and the expected outputs.

**Do not let the reporting layer calculate business metrics.**
Reporting communicates results. The SQL/rules layer produces them.

**Do not introduce an LLM.**
Any LLM experiment must be a separate, optional add-on and must never replace the verified pipeline.

**Do not hide inactive resellers.**
The `LEFT JOIN` in `02_reseller_activity.sql` is intentional. Changing it to an `INNER JOIN` would make `R024` disappear.

**Do not recreate completed parts** unless a bug is found. Build on the existing implementation.

---

## 16. Target Architecture

```text
                    DATA GENERATOR
                         |
                         v
              resellers.csv / orders.csv
                         |
                         v
                  DATA VALIDATION
                         |
                         v
                  SQLite DATABASE
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
      CATEGORY       RESELLER        REGION
        SQL            SQL             SQL
          |              |              |
          +--------------+--------------+
                         |
                         v
                  PYTHON RULES
                         |
             +-----------+-----------+
             |           |           |
             v           v           v
          Category   Inactive     Regional
           Alerts    Resellers     Alerts
             |           |           |
             +-----------+-----------+
                         |
                         v
                  ALERT COLLECTION
                         |
                         v
             DETERMINISTIC REPORTING
                         |
                         v
                REPORT VALIDATION
                         |
                         v
                 MOCK ORCHESTRATOR
                         |
                         v
                   HUMAN REVIEW
```

---

## 17. Definition of Done

- [x] Dataset generates successfully
- [x] Dataset validation passes
- [x] SQLite database builds successfully
- [x] All current SQL queries execute successfully
- [x] Category rules work
- [x] Inactive reseller rule works
- [ ] pytest test suite passes
- [ ] Regional MoM is implemented
- [ ] Regional rules work
- [ ] Alerts are persisted
- [ ] Deterministic report is generated
- [ ] Report values are validated
- [ ] Agent specification exists
- [ ] Mock runner executes the workflow
- [ ] One command runs the complete pipeline
- [ ] Example outputs are included
- [ ] README explains the final architecture
- [ ] GitHub repository is clean
