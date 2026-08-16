import sqlite3
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SQL_DIR = BASE / "sql"

db_file = SQL_DIR / "sales.db"
query_file = SQL_DIR / "queries.sql"
output_file = SQL_DIR / "SQL_Results.xlsx"
EXPECTED_QUERY_COUNT = 7

if not db_file.exists():
    raise FileNotFoundError(f"Database not found: {db_file}")

if not query_file.exists():
    raise FileNotFoundError(f"SQL query file not found: {query_file}")

sql_text = query_file.read_text(encoding="utf-8")

clean_lines = []
for line in sql_text.splitlines():
    if line.strip().startswith("--"):
        continue
    clean_lines.append(line)

clean_sql = "\n".join(clean_lines)

queries = [
    q.strip()
    for q in clean_sql.split(";")
    if q.strip()
]

valid_queries = []
for query in queries:
    query_start = query.lstrip().upper()
    if query_start.startswith("SELECT") or query_start.startswith("WITH"):
        valid_queries.append(query)

if not valid_queries:
    raise ValueError(
        "No SELECT or WITH queries were found in queries.sql. "
        "Check the SQL file format."
    )

if len(valid_queries) != EXPECTED_QUERY_COUNT:
    raise ValueError(
        f"Expected {EXPECTED_QUERY_COUNT} SQL business queries, "
        f"but found {len(valid_queries)}."
    )

print("TASK-2 SQL RESULT GENERATION")
print("=" * 50)
print(f"SQL queries detected: {len(valid_queries)}")

conn = sqlite3.connect(db_file)

try:
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for result_number, query in enumerate(valid_queries, start=1):
            sheet_name = f"Q{result_number}"
            print(f"\nRunning {sheet_name}...")

            try:
                result = pd.read_sql_query(query, conn)
            except Exception as e:
                raise RuntimeError(
                    f"{sheet_name} failed.\n"
                    f"SQL:\n{query}\n\n"
                    f"Error: {e}"
                ) from e

            if result.empty:
                print(f"{sheet_name}: WARNING, query returned 0 rows.")
            else:
                print(f"{sheet_name}: {len(result)} rows generated.")

            result.to_excel(writer, sheet_name=sheet_name, index=False)
finally:
    conn.close()

print("\n" + "=" * 50)
print("SQL results successfully generated.")
print(f"Queries processed: {len(valid_queries)}")
print(f"Output file: {output_file}")
print("=" * 50)