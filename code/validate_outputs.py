import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
excel_file = BASE / "ApexPlanet_DataAnalytics_Dataset.xlsx"
db_file = BASE / "sql" / "sales.db"
report_dir = BASE / "report"
report_dir.mkdir(parents=True, exist_ok=True)

EXPECTED_MISSING_AGE = 20
EXPECTED_MISSING_CITY = 13
EXPECTED_PROBLEMATIC_ORDER_IDS = 1
EXPECTED_SQL_QUERY_COUNT = 7

if not excel_file.exists():
    raise FileNotFoundError(f"Dataset not found: {excel_file}")
if not db_file.exists():
    raise FileNotFoundError(f"Database not found: {db_file}")

df = pd.read_excel(excel_file)

required_columns = [
    "Order_ID", "Order_Date", "Customer_ID", "Customer_Name",
    "Age", "Gender", "City", "Product", "Category",
    "Quantity", "Unit_Price", "Total_Sales"
]

missing_source_columns = [c for c in required_columns if c not in df.columns]
if missing_source_columns:
    raise ValueError(f"Missing source columns: {missing_source_columns}")

# Source-data quality validation.
dates = pd.to_datetime(df["Order_Date"], errors="coerce")
invalid_dates = int(dates.isna().sum())
duplicate_rows = int(df.duplicated().sum())
missing_age = int(df["Age"].isna().sum())
missing_city = int(df["City"].isna().sum())
zero_quantity = int((df["Quantity"] == 0).sum())
negative_quantity = int((df["Quantity"] < 0).sum())
zero_price = int((df["Unit_Price"] == 0).sum())
negative_price = int((df["Unit_Price"] < 0).sum())

calculated_sales = df["Quantity"] * df["Unit_Price"]
sales_difference = (calculated_sales - df["Total_Sales"]).abs()
incorrect_sales = int((sales_difference > 0.01).sum())

order_quality = (
    df.groupby("Order_ID")
    .agg(
        Customer_Count=("Customer_ID", "nunique"),
        Date_Count=("Order_Date", "nunique")
    )
)

invalid_orders = order_quality[
    (order_quality["Customer_Count"] > 1)
    | (order_quality["Date_Count"] > 1)
]
problematic_order_id_count = int(len(invalid_orders))

conn = sqlite3.connect(db_file)

try:
    db_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM sales", conn
    ).iloc[0]["n"]

    db_revenue = pd.read_sql_query(
        "SELECT SUM(Total_Sales) AS revenue FROM sales", conn
    ).iloc[0]["revenue"]

    db_units = pd.read_sql_query(
        "SELECT SUM(Quantity) AS units FROM sales", conn
    ).iloc[0]["units"]

    db_average_transaction = pd.read_sql_query(
        "SELECT AVG(Total_Sales) AS average_transaction FROM sales", conn
    ).iloc[0]["average_transaction"]

    db_customer_count = pd.read_sql_query(
        "SELECT COUNT(DISTINCT Customer_ID) AS customers FROM sales", conn
    ).iloc[0]["customers"]

    db_order_count = pd.read_sql_query(
        "SELECT COUNT(DISTINCT Order_ID) AS orders FROM sales", conn
    ).iloc[0]["orders"]

    sales_columns = [row[1] for row in conn.execute("PRAGMA table_info(sales)")]

    required_sales_columns = [
        "Transaction_ID", "Order_ID", "Order_Date", "Customer_ID",
        "Product", "Quantity", "Unit_Price", "Total_Sales"
    ]

    required_tables = {"customers", "products", "orders", "sales"}
    actual_tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }

    customer_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM customers", conn
    ).iloc[0]["n"]
    product_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM products", conn
    ).iloc[0]["n"]
    order_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM orders", conn
    ).iloc[0]["n"]
    sales_rows = pd.read_sql_query(
        "SELECT COUNT(*) AS n FROM sales", conn
    ).iloc[0]["n"]

    orphan_customers = pd.read_sql_query(
        """
        SELECT COUNT(*) AS n
        FROM sales s
        LEFT JOIN customers c
            ON s.Customer_ID = c.Customer_ID
        WHERE c.Customer_ID IS NULL
        """,
        conn
    ).iloc[0]["n"]

    orphan_products = pd.read_sql_query(
        """
        SELECT COUNT(*) AS n
        FROM sales s
        LEFT JOIN products p
            ON s.Product = p.Product
        WHERE p.Product IS NULL
        """,
        conn
    ).iloc[0]["n"]
finally:
    conn.close()

# SQL result workbook validation.
sql_results_file = BASE / "sql" / "SQL_Results.xlsx"
required_sql_sheets = {
    f"Q{i}" for i in range(1, EXPECTED_SQL_QUERY_COUNT + 1)
}

if sql_results_file.exists():
    sql_workbook = pd.ExcelFile(sql_results_file)
    actual_sql_sheets = set(sql_workbook.sheet_names)
    sql_sheets_present = required_sql_sheets.issubset(actual_sql_sheets)

    sql_sheets_non_empty = True
    for sheet in required_sql_sheets:
        if sheet in actual_sql_sheets:
            result_df = pd.read_excel(sql_results_file, sheet_name=sheet)
            if result_df.empty:
                sql_sheets_non_empty = False
else:
    sql_sheets_present = False
    sql_sheets_non_empty = False

checks = {
    "Duplicate rows check": duplicate_rows == 0,
    "Missing Age check": missing_age == EXPECTED_MISSING_AGE,
    "Missing City check": missing_city == EXPECTED_MISSING_CITY,
    "Invalid dates check": invalid_dates == 0,
    "Zero quantity check": zero_quantity == 0,
    "Negative quantity check": negative_quantity == 0,
    "Zero unit price check": zero_price == 0,
    "Negative unit price check": negative_price == 0,
    "Total_Sales calculation check": incorrect_sales == 0,
    "Order_ID integrity check": (
        problematic_order_id_count == EXPECTED_PROBLEMATIC_ORDER_IDS
    ),
    "Row count matches": db_rows == len(df),
    "Revenue matches": abs(db_revenue - df["Total_Sales"].sum()) < 0.01,
    "Units match": db_units == df["Quantity"].sum(),
    "Average transaction value matches": abs(
        db_average_transaction - df["Total_Sales"].mean()
    ) < 0.01,
    "Customer count matches": db_customer_count == df["Customer_ID"].nunique(),
    "Distinct Order ID count matches": db_order_count == df["Order_ID"].nunique(),
    "Required sales columns exist": all(
        c in sales_columns for c in required_sales_columns
    ),
    "Required database tables exist": required_tables.issubset(actual_tables),
    "Source columns exist": len(missing_source_columns) == 0,
    "Customers table populated": customer_rows > 0,
    "Products table populated": product_rows > 0,
    "Orders table reconciled": order_rows == df["Order_ID"].nunique(),
    "Sales table reconciled": sales_rows == len(df),
    "No orphan customer records": orphan_customers == 0,
    "No orphan product records": orphan_products == 0,
    "SQL results workbook exists": sql_results_file.exists(),
    "All 7 SQL result sheets exist": sql_sheets_present,
    "All SQL result sheets contain data": sql_sheets_non_empty,
}

print("TASK-2 FINAL OUTPUT VALIDATION")
print("=" * 60)

all_passed = True
for name, result in checks.items():
    status = "PASS" if result else "FAIL"
    print(f"{name}: {status}")
    if not result:
        all_passed = False

validation_file = report_dir / "Validation_Report.txt"

with open(validation_file, "w", encoding="utf-8") as f:
    f.write("TASK-2 FINAL VALIDATION REPORT\n")
    f.write("=" * 50 + "\n\n")
    f.write("SOURCE DATA SUMMARY\n")
    f.write("-" * 30 + "\n")
    f.write(f"Records: {len(df):,}\n")
    f.write(f"Customers: {df['Customer_ID'].nunique():,}\n")
    f.write(f"Distinct Order IDs: {df['Order_ID'].nunique():,}\n")
    f.write(f"Revenue: ₹{df['Total_Sales'].sum():,.2f}\n")
    f.write(f"Units Sold: {df['Quantity'].sum():,}\n")
    f.write(f"Missing Age: {missing_age}\n")
    f.write(f"Missing City: {missing_city}\n")
    f.write(f"Problematic Order IDs: {problematic_order_id_count}\n\n")
    f.write("VALIDATION RESULTS\n")
    f.write("-" * 30 + "\n")
    for name, result in checks.items():
        status = "PASS" if result else "FAIL"
        f.write(f"{name}: {status}\n")
    f.write("\n")
    f.write(
        "ALL VALIDATION CHECKS PASSED.\n"
        if all_passed
        else "ONE OR MORE VALIDATION CHECKS FAILED.\n"
    )

if not all_passed:
    raise ValueError(f"Validation failed. Review: {validation_file}")

print("\nAll validation checks passed.")
print("\nValidation report saved to:")
print(validation_file)