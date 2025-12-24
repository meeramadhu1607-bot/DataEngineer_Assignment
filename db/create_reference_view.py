import sqlite3
from pathlib import Path

DB_PATH = Path("investment.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE VIEW IF NOT EXISTS reference_prices AS
SELECT
    SYMBOL AS instrument_key,
    DATETIME AS price_date,
    PRICE AS price
FROM equity_prices

UNION ALL

SELECT
    ISIN AS instrument_key,
    DATETIME AS price_date,
    PRICE AS price
FROM bond_prices;
""")

conn.commit()
conn.close()

print("✅ reference_prices view created correctly")
