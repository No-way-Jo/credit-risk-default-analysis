# Credit & Loan Default Risk Analysis (SQL)

A large-scale financial risk assessment portfolio project utilizing advanced SQL query optimization to evaluate default rates, risk escalation matrices, and capital loss exposure metrics across 32,000+ consumer loan records.

## Analytical & Engineering Capabilities
* **Risk Tier Escalation Matrix:** Implements Common Table Expressions (CTEs) to isolate exponential default rate trends across deteriorating credit asset tiers (Grades A-G).
* **Financial Leverage Exposure Auditing:** Programs conditional logic (`CASE WHEN`) and multi-stage data aggregation scripts to segment borrower debt-to-income (DTI) thresholds and calculate absolute institutional capital-at-loss exposure.
* **Agile Data Pipeline Execution:** Integrates a high-performance in-memory SQL engine (`DuckDB`) with Python `Pandas` structures to handle large-scale database operations without server overhead.

## Project File Layout
* `risk_audit.py`: Complete Python and embedded SQL source code containing data ingestion pipelines and risk aggregation logic.
* `credit_grade_risk_matrix.csv`: Generated output data file tracking default volumes and scaling percentages by risk grade.
* `leverage_loss_exposure.csv`: Generated output data file evaluating financial risk tiers against average incomes and absolute losses.

## Core Technologies
* **Query Optimization:** SQL (DuckDB Database Core Engine)
* **Data Engineering:** Python, Pandas
