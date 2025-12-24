import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("investment.db")
OUTPUT_PATH = Path("output/price_reconciliation.csv")

def price_reconciliation():
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        fp.fund_name,
        fp.symbol,
        fp.position_date,
        fp.price AS fund_price,

        (
            SELECT rp.price
            FROM reference_prices rp
            WHERE rp.instrument_key = fp.symbol
              AND rp.price_date <= fp.position_date
            ORDER BY rp.price_date DESC
            LIMIT 1
        ) AS reference_price,

        fp.price -
        (
            SELECT rp.price
            FROM reference_prices rp
            WHERE rp.instrument_key = fp.symbol
              AND rp.price_date <= fp.position_date
            ORDER BY rp.price_date DESC
            LIMIT 1
        ) AS price_difference

    FROM fund_positions fp
    ORDER BY fp.fund_name, fp.position_date;
    """

    df = pd.read_sql_query(query, conn)
    df.to_csv(OUTPUT_PATH, index=False)

    conn.close()
    print("✅ Price reconciliation CSV generated")

if __name__ == "__main__":
    price_reconciliation()
