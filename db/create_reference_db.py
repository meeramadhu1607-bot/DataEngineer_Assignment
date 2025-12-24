import sqlite3
from pathlib import Path

# This is the SQLite database file that will be CREATED
DB_PATH = Path("investment.db")

# This is the SQL file you RECEIVED
REFERENCE_SQL_PATH = Path("data/master-reference-sql.sql")

def create_database():
    # 1. Connect to SQLite
    # If investment.db does not exist, SQLite creates it
    conn = sqlite3.connect(DB_PATH)

    # 2. Read the SQL file
    with open(REFERENCE_SQL_PATH, "r") as f:
        sql_script = f.read()

    # 3. Execute all SQL statements in the file
    conn.executescript(sql_script)

    # 4. Save and close
    conn.commit()
    conn.close()

    print("✅ Database created and reference tables loaded.")

if __name__ == "__main__":
    create_database()
