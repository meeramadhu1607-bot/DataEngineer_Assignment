import sqlite3
from pathlib import Path

DB_PATH = Path("investment.db")

def create_fund_positions_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fund_positions (
        fund_name TEXT,
        financial_type TEXT,
        symbol TEXT,
        security_name TEXT,
        instrument_id TEXT,   -- SEDOL or ISIN
        position_date DATE,
        price REAL,
        quantity REAL,
        market_value REAL,
        realized_pnl REAL
    );
    """)

    conn.commit()
    conn.close()
    print("✅ fund_positions table created")

if __name__ == "__main__":
    create_fund_positions_table()
