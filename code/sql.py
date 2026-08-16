import pandas as pd
import sqlite3

from pathlib import Path

# ==================================================
# Project paths
# ==================================================

BASE = Path(__file__).resolve().parent.parent
file = BASE / "ApexPlanet_DataAnalytics_Dataset.xlsx"
SQL_DIR = BASE / "sql"
SQL_DIR.mkdir(parents=True, exist_ok=True)

db_file = SQL_DIR / "sales.db"

# ==================================================
# Read and prepare dataset
# ==================================================

df = pd.read_excel(file)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

required_columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Customer_Name",
    "Age",
    "Gender",
    "City",
    "Product",
    "Category",
    "Quantity",
    "Unit_Price",
    "Total_Sales"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

invalid_dates = df["Order_Date"].isna().sum()

if invalid_dates > 0:
    raise ValueError(
        f"Found {invalid_dates} invalid Order_Date values."
    )

# Create transaction ID for row-level traceability.
df.insert(
    0,
    "Transaction_ID",
    range(1, len(df) + 1)
)

# ==================================================
# Create Customers table
# ==================================================

customer_quality = (
    df.groupby("Customer_ID")
    .agg(
        Name_Variants=("Customer_Name", "nunique"),
        Age_Variants=("Age", "nunique"),
        Gender_Variants=("Gender", "nunique"),
        City_Variants=("City", "nunique")
    )
)

customers = (
    df.sort_values("Transaction_ID")
    .groupby("Customer_ID")
    .nth(0)
    .reset_index()
    [[
        "Customer_ID",
        "Customer_Name",
        "Age",
        "Gender",
        "City"
    ]]
)

customers = customers.merge(
    customer_quality.reset_index(),
    on="Customer_ID",
    how="left"
)

customers["Profile_Status"] = "OK"

customers.loc[
    (
        (customers["Name_Variants"] > 1) |
        (customers["Age_Variants"] > 1) |
        (customers["Gender_Variants"] > 1) |
        (customers["City_Variants"] > 1)
    ),
    "Profile_Status"
] = "CHECK"

# ==================================================
# Create Products table
# Unit_Price is excluded because price varies by transaction.
# ==================================================

products = (
    df[["Product", "Category"]]
    .drop_duplicates("Product")
    .sort_values("Product")
)

# ==================================================
# Create Orders reference table
# Order_ID is not fully reliable in the source dataset.
# The table records conflict counts instead of hiding them.
# ==================================================

order_quality = (
    df.groupby("Order_ID")
    .agg(
        Record_Count=("Transaction_ID", "size"),
        Customer_Count=("Customer_ID", "nunique"),
        Date_Count=("Order_Date", "nunique")
    )
    .reset_index()
)

order_first_observation = (
    df.sort_values("Transaction_ID")
    .groupby("Order_ID")
    .nth(0)
    .reset_index()
    [[
        "Order_ID",
        "Order_Date",
        "Customer_ID"
    ]]
)

orders = order_first_observation.merge(
    order_quality,
    on="Order_ID",
    how="left"
)

orders["Order_ID_Status"] = "OK"
orders.loc[
    (
        (orders["Customer_Count"] > 1) |
        (orders["Date_Count"] > 1)
    ),
    "Order_ID_Status"
] = "CHECK"

# ==================================================
# Create Sales table
# Keep customer attributes at transaction level.
# This prevents conflicting Customer_ID profiles from
# changing the row-level analytical results.
# ==================================================

sales = df[
    [
        "Transaction_ID",
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Customer_Name",
        "Age",
        "Gender",
        "City",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Total_Sales"
    ]
]

# ==================================================
# Reconciliation checks
# ==================================================

if len(orders) != df["Order_ID"].nunique():
    raise ValueError(
        "Orders table reconciliation failed."
    )

if len(customers) != df["Customer_ID"].nunique():
    raise ValueError(
        "Customers table reconciliation failed."
    )

if len(products) != df["Product"].nunique():
    raise ValueError(
        "Products table reconciliation failed."
    )

if len(sales) != len(df):
    raise ValueError(
        "Sales table reconciliation failed."
    )

# ==================================================
# Create SQLite database
# ==================================================

conn = sqlite3.connect(db_file)

try:
    customers.to_sql(
        "customers",
        conn,
        if_exists="replace",
        index=False
    )

    products.to_sql(
        "products",
        conn,
        if_exists="replace",
        index=False
    )

    orders.to_sql(
        "orders",
        conn,
        if_exists="replace",
        index=False
    )

    sales.to_sql(
        "sales",
        conn,
        if_exists="replace",
        index=False
    )

    # Useful indexes for joins and filtering.
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_order_id "
        "ON sales(Order_ID)"
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_customer_id "
        "ON sales(Customer_ID)"
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_product "
        "ON sales(Product)"
    )

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_sales_order_date "
        "ON sales(Order_Date)"
    )

    conn.commit()

finally:
    conn.close()

# ==================================================
# Database schema validation
# ==================================================

conn = sqlite3.connect(db_file)

try:
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table'"
        )
    }

    required_tables = {
        "customers",
        "products",
        "orders",
        "sales"
    }

    missing_tables = required_tables - tables

    if missing_tables:
        raise ValueError(
            f"Missing database tables: {sorted(missing_tables)}"
        )

    sales_columns = [
        row[1]
        for row in conn.execute(
            "PRAGMA table_info(sales)"
        )
    ]

    required_sales_columns = [
        "Transaction_ID",
        "Order_ID",
        "Order_Date",
        "Customer_ID",
        "Customer_Name",
        "Age",
        "Gender",
        "City",
        "Product",
        "Category",
        "Quantity",
        "Unit_Price",
        "Total_Sales"
    ]

    missing_sales_columns = [
        col
        for col in required_sales_columns
        if col not in sales_columns
    ]

    if missing_sales_columns:
        raise ValueError(
            "Missing sales columns: "
            f"{missing_sales_columns}"
        )

finally:
    conn.close()

# ==================================================
# Final summary
# ==================================================

print("DATABASE CREATED SUCCESSFULLY")
print("=" * 50)
print("Database:", db_file)
print("Tables: customers, products, orders, sales")

print("\nROW COUNTS")
print("=" * 50)
print("Customers:", len(customers))
print("Products:", len(products))
print("Distinct Order IDs:", len(orders))
print("Sales transactions:", len(sales))

print("\nDATA QUALITY FLAGS")
print("=" * 50)
print(
    "Customer profiles needing review:",
    (customers["Profile_Status"] == "CHECK").sum()
)
print(
    "Order IDs needing review:",
    (orders["Order_ID_Status"] == "CHECK").sum()
)

print("\nRECONCILIATION")
print("=" * 50)
print("Dataset rows:", len(df))
print("Distinct orders:", df["Order_ID"].nunique())
print("Distinct customers:", df["Customer_ID"].nunique())
print("Total units:", df["Quantity"].sum())
print("Total revenue:", round(df["Total_Sales"].sum(), 2))

print("\nDatabase creation completed successfully.")
