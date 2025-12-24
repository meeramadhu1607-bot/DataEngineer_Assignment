import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("investment.db")
OUTPUT_PATH = Path("output/best_fund_by_month.csv")

def best_fund_analysis():
    conn = sqlite3.connect(DB_PATH)

    query = """
    WITH fund_monthly AS (
        SELECT
            fund_name,
            strftime('%Y-%m', position_date) AS month,
            SUM(market_value) AS fund_market_value,
            SUM(realized_pnl) AS fund_realized_pnl
        FROM fund_positions
        GROUP BY fund_name, month
    ),
    fund_returns AS (
        SELECT
            fund_name,
            month,
            fund_market_value AS mv_end,
            LAG(fund_market_value)
                OVER (PARTITION BY fund_name ORDER BY month)
                AS mv_start,
            fund_realized_pnl
        FROM fund_monthly
    )
    SELECT
        fund_name,
        month,
        (mv_end - mv_start + fund_realized_pnl) * 1.0 / mv_start
            AS rate_of_return
    FROM fund_returns
    WHERE mv_start IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)

    # Rank funds per month
    df["rank"] = df.groupby("month")["rate_of_return"] \
                    .rank(method="first", ascending=False)

    best_funds = df[df["rank"] == 1]

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    best_funds.to_csv(OUTPUT_PATH, index=False)

    conn.close()
    print("✅ Best performing fund analysis generated")

if __name__ == "__main__":
    best_fund_analysis()
