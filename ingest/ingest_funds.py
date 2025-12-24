import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("investment.db")
FUNDS_DIR = Path("data/external-funds")

def ingest_funds():
    conn = sqlite3.connect(DB_PATH)

    for csv_file in FUNDS_DIR.glob("*.csv"):
        df = pd.read_csv(csv_file)

        # Normalize column names
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

        # Handle ISIN / SEDOL mismatch
        if "sedol" in df.columns:
            df["instrument_id"] = df["sedol"]
        elif "isin" in df.columns:
            df["instrument_id"] = df["isin"]
        else:
            raise ValueError(f"No instrument id found in {csv_file.name}")

        # Add fund name from file name
        df["fund_name"] = csv_file.stem

        # Rename columns to match DB
        df = df.rename(columns={
            "financial_type": "financial_type",
            "symbol": "symbol",
            "security_name": "security_name",
            "price": "price",
            "quantity": "quantity",
            "market_value": "market_value",
            "realised_p/l": "realized_pnl",
        })

        # Select only DB columns
        df = df[
            [
                "fund_name",
                "financial_type",
                "symbol",
                "security_name",
                "instrument_id",
                "price",
                "quantity",
                "market_value",
                "realized_pnl"
            ]
        ]

        df.to_sql(
            "fund_positions",
            conn,
            if_exists="append",
            index=False
        )

        print(f"✅ Ingested {csv_file.name}")

    conn.close()
    print("🎉 All fund data ingested successfully")

if __name__ == "__main__":
    ingest_funds()
