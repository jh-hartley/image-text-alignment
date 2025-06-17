import sys
from pathlib import Path

import psycopg2

from src.config import config


def copy_csv_to_postgres(csv_path: str | Path, table_name: str) -> None:
    """
    Bulk load a CSV file into a PostgreSQL table using COPY.
    Assumes the table already exists and matches the CSV columns
    exactly.

    Note, this does not validate the data, but it uploads
    extremely quickly.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        print(f"CSV file not found: {csv_path}")
        sys.exit(1)

    conn = None
    try:
        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )

        cur = conn.cursor()
        with csv_path.open("r", encoding="utf-8-sig") as f:
            sql = f"COPY {table_name} FROM STDIN WITH CSV HEADER"
            cur.copy_expert(sql, f)
        conn.commit()
        print(f"Successfully loaded {csv_path} into {table_name}")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python ingest_csvs.py " "<csv_file_path> <table_name>")
        sys.exit(1)
    csv_file = sys.argv[1]
    table = sys.argv[2]
    copy_csv_to_postgres(csv_file, table)
