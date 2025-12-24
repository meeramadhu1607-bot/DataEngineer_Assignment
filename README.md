Data Engineering Home Assignment – Fund Analytics
Overview

This project implements a data ingestion and analytics pipeline for an investment firm that receives monthly position reports from 10 funds.
The goal is to:

Store reference data (bonds & equities)
Ingest monthly fund position CSVs
Perform price reconciliation
Identify the best-performing fund per month

The solution is built using Python + SQLite + SQL, following data engineering best practices.

📁 Project Structure
python_assignment/
│
├── data/
│   ├── external-funds/              # Raw fund CSV files (input)
│   └── master-reference-sql.sql     # Reference data DDL + inserts
│
├── db/
│   ├── create_reference_db.py       # Creates reference tables
│   ├── create_fund_table.py         # Creates fund_positions table
│   └── create_reference_view.py     # Creates reference_prices view
│
├── ingest/
│   └── ingest_funds.py              # Loads fund CSVs into SQLite
│
├── analysis/
│   ├── price_reconciliation.py      # Price vs reference comparison
│   └── best_fund_by_month.py        # Best fund per month analysis
│
├── output/
│   ├── price_reconciliation.csv
│   └── best_fund_by_month.csv
│
├── investment.db                    # SQLite database (generated)
└── README.md

🧠 Data Model
Reference Tables (from provided SQL)
equity_reference
equity_prices
bond_reference
bond_prices
Fund Positions Table
fund_positions (
    fund_name TEXT,
    financial_type TEXT,
    symbol TEXT,
    security_name TEXT,
    sedol TEXT,
    position_date DATE,
    price REAL,
    quantity REAL,
    market_value REAL,
    realized_pnl REAL
)

Reference Prices View
A unified view combining equity and bond prices:
reference_prices(symbol, price_date, price)


Run the scripts in this exact order:

Step 1: Create Reference Tables
python db/create_reference_db.py


✔ Creates investment.db
✔ Loads reference data from master-reference-sql.sql

Step 2: Create Fund Positions Table
python db/create_fund_table.py


✔ Creates fund_positions table

Step 3: Create Reference Price View
python db/create_reference_view.py


✔ Creates reference_prices view for analytics

Step 4: Ingest Fund CSV Files
python ingest/ingest_funds.py


✔ Reads all CSVs from data/external-funds/
✔ Extracts fund name & date from filenames
✔ Handles ISIN / SEDOL differences
✔ Loads data into fund_positions

Step 5: Run Price Reconciliation
python analysis/price_reconciliation.py


📄 Output:

output/price_reconciliation.csv


Logic

Compares fund-reported price vs reference price

Uses last available reference price if EOM price is missing

Calculates price differences

Step 6: Best Performing Fund by Month
python analysis/best_fund_by_month.py


📄 Output:

output/best_fund_by_month.csv


Formula Used

Rate of Return =
(Fund_MV_end - Fund_MV_start + Realized_PnL) / Fund_MV_start

📌 Key Design Decisions

SQLite used for simplicity and portability

Schema normalized for analytics

View used to unify bond & equity prices

Filename-driven date extraction to avoid reliance on CSV content

Python handles orchestration, SQL handles aggregation


🔮 Production Gaps & Improvements

Replace SQLite with Snowflake / PostgreSQL

Use dbt for transformations

Add data quality checks

Parameterize file ingestion

CI/CD integration

Incremental loads & partitioning

Logging & monitoring

🛠 Tech Stack

Python 3.x

SQLite

Pandas

SQL