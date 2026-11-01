import pandas as pd
import tabulate
import sqlite3
from pathlib import Path

CSV_PATH = Path("../MetObjects.csv")
DB_PATH = "themetsql.db"
TABLE_NAME = "MetObjects"
CHUNK_SIZE = 1000

# read csv file into pandas dataframe
df = pd.read_csv("../MetObjects.csv", 
                 dtype=str, 
                 skip_blank_lines=False, 
                 nrows=20, 
                 usecols=["Object Number", "Object Name", "Title", "Country"])

def import_csv_to_sqlite():
    total_rows = 0

    with sqlite3.connect(DB_PATH) as connection:

        # Read the CSV file in smaller chunks
        chunks = pd.read_csv(
            CSV_PATH,
            dtype=str,
            chunksize=CHUNK_SIZE,
            low_memory=False
        )

        for chunk_number, chunk in enumerate(chunks, start=1):

            # First chunk creates/replaces the table.
            # Remaining chunks append data.
            if_exists = "replace" if chunk_number == 1 else "append"

            # Here's where we get our columns automatically from the CSV file and create the table in SQLite.
            chunk.to_sql(
                name=TABLE_NAME,
                con=connection,
                if_exists=if_exists,
                index=False,
                method="multi",
                chunksize=100 #Inserts 100 rows at a time for better performance
            )

            total_rows += len(chunk)

            print(f"Chunk {chunk_number}: {total_rows} rows imported")

        print(f"\nImport completed: {total_rows} rows")

def verify_database():
    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.cursor()

        # Check if the table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}'")
        table_exists = cursor.fetchone() is not None

        if table_exists:
            print(f"Table '{TABLE_NAME}' exists in the database.")
        else:
            print(f"Table '{TABLE_NAME}' does not exist in the database.")
    #How many rows are in the database after import?
    with sqlite3.connect("themetsql.db") as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM "MetObjects"')

        count = cursor.fetchone()[0]

        print(f"Total objects in database: {count}")

    #What are the columns in the database?
    with sqlite3.connect("themetsql.db") as connection:
        cursor = connection.execute('PRAGMA table_info("MetObjects")')

        for column in cursor.fetchall():
            print(column[1], column[2])

def main():
    if not CSV_PATH.is_file():
        print(f"CSV file not found: {CSV_PATH}")
        return

    import_csv_to_sqlite()
    verify_database()

if __name__ == "__main__":
    main()