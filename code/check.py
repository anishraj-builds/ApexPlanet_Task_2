import pandas as pd
from pathlib import Path

# ==================================================
# Project paths
# ==================================================

BASE = Path(__file__).resolve().parent.parent
file = BASE / "ApexPlanet_DataAnalytics_Dataset.xlsx"
REPORT_DIR = BASE / "report"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ==================================================
# Read dataset
# ==================================================

df = pd.read_excel(file)
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# ==================================================
# Basic information
# ==================================================

print("DATASET OVERVIEW")
print("=" * 50)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# ==================================================
# Missing values
# ==================================================

missing_values = df.isnull().sum()

print("\nMISSING VALUES")
print("=" * 50)
print(missing_values)

# ==================================================
# Duplicate rows
# ==================================================

duplicate_rows = df.duplicated().sum()

print("\nDuplicate rows:", duplicate_rows)

# ==================================================
# Unique values
# ==================================================

print("\nUNIQUE VALUES")
print("=" * 50)
print("Transactions:", len(df))
print("Distinct Order IDs:", df["Order_ID"].nunique())
print("Customers:", df["Customer_ID"].nunique())
print("Products:", df["Product"].nunique())
print("Categories:", df["Category"].nunique())
print("Cities:", df["City"].nunique(dropna=True))
print("Gender:", df["Gender"].nunique(dropna=True))

# ==================================================
# Date validation
# ==================================================

print("\nDATE RANGE")
print("=" * 50)
print("Start:", df["Order_Date"].min().date())
print("End:", df["Order_Date"].max().date())
print("Invalid dates:", df["Order_Date"].isna().sum())

# ==================================================
# Quantity check
# ==================================================

zero_quantity = (df["Quantity"] == 0).sum()
negative_quantity = (df["Quantity"] < 0).sum()

print("\nQUANTITY CHECK")
print("=" * 50)
print("Minimum:", df["Quantity"].min())
print("Maximum:", df["Quantity"].max())
print("Zero:", zero_quantity)
print("Negative:", negative_quantity)

# ==================================================
# Unit price check
# ==================================================

zero_price = (df["Unit_Price"] == 0).sum()
negative_price = (df["Unit_Price"] < 0).sum()

print("\nUNIT PRICE CHECK")
print("=" * 50)
print("Minimum:", df["Unit_Price"].min())
print("Maximum:", df["Unit_Price"].max())
print("Zero:", zero_price)
print("Negative:", negative_price)

# ==================================================
# Sales validation
# ==================================================

calculated_sales = df["Quantity"] * df["Unit_Price"]
difference = (calculated_sales - df["Total_Sales"]).abs()
incorrect_sales = (difference > 0.01).sum()

print("\nSALES VALIDATION")
print("=" * 50)
print("Incorrect sales calculations:", incorrect_sales)

# ==================================================
# Repeated Order IDs
# ==================================================

duplicates = df[df["Order_ID"].duplicated(keep=False)].copy()

print("\nREPEATED ORDER IDs")
print("=" * 50)
print("Records involved:", len(duplicates))
print("Unique repeated Order IDs:", duplicates["Order_ID"].nunique())

# ==================================================
# Order ID integrity
# ==================================================

order_check = (
    df.groupby("Order_ID")
    .agg(
        Record_Count=("Transaction_ID", "size")
        if "Transaction_ID" in df.columns
        else ("Order_ID", "size"),
        Customer_Count=("Customer_ID", "nunique"),
        Date_Count=("Order_Date", "nunique")
    )
)

invalid_orders = order_check[
    (order_check["Customer_Count"] > 1) |
    (order_check["Date_Count"] > 1)
].copy()

print("\nORDER ID INTEGRITY")
print("=" * 50)
print(
    "Order IDs with multiple customers or dates:",
    len(invalid_orders)
)

if len(invalid_orders) > 0:
    print("\nProblematic Order IDs:")
    print(invalid_orders)

# ==================================================
# Customer profile consistency
# ==================================================

customer_profile = (
    df.groupby("Customer_ID")
    .agg(
        Name_Variants=("Customer_Name", "nunique"),
        Age_Variants=("Age", "nunique"),
        Gender_Variants=("Gender", "nunique"),
        City_Variants=("City", "nunique")
    )
)

inconsistent_customers = customer_profile[
    (customer_profile["Name_Variants"] > 1) |
    (customer_profile["Age_Variants"] > 1) |
    (customer_profile["Gender_Variants"] > 1) |
    (customer_profile["City_Variants"] > 1)
].copy()

print("\nCUSTOMER PROFILE CONSISTENCY")
print("=" * 50)
print(
    "Customers with conflicting profile attributes:",
    len(inconsistent_customers)
)

if len(inconsistent_customers) > 0:
    print(inconsistent_customers.head(20))

# ==================================================
# Create detailed data-quality report
# ==================================================

quality_report = pd.DataFrame({
    "Check": [
        "Total Rows",
        "Total Columns",
        "Missing Age",
        "Missing City",
        "Duplicate Rows",
        "Invalid Dates",
        "Zero Quantity",
        "Negative Quantity",
        "Zero Unit Price",
        "Negative Unit Price",
        "Incorrect Total Sales",
        "Distinct Order IDs",
        "Problematic Order IDs",
        "Customers with Conflicting Profiles"
    ],
    "Value": [
        len(df),
        len(df.columns),
        df["Age"].isna().sum(),
        df["City"].isna().sum(),
        duplicate_rows,
        df["Order_Date"].isna().sum(),
        zero_quantity,
        negative_quantity,
        zero_price,
        negative_price,
        incorrect_sales,
        df["Order_ID"].nunique(),
        len(invalid_orders),
        len(inconsistent_customers)
    ]
})

quality_report.to_excel(
    REPORT_DIR / "Data_Quality_Report.xlsx",
    index=False
)

# Save problematic order details
if len(invalid_orders) > 0:
    problematic_order_ids = (
        df[df["Order_ID"].isin(invalid_orders.index)]
        .sort_values(["Order_ID", "Order_Date"])
    )
else:
    problematic_order_ids = pd.DataFrame(
        columns=df.columns
    )

problematic_order_ids.to_excel(
    REPORT_DIR / "Problematic_Order_IDs.xlsx",
    index=False
)

# Save customer consistency details
if len(inconsistent_customers) > 0:
    problematic_customer_ids = (
        df[df["Customer_ID"].isin(inconsistent_customers.index)]
        .sort_values(["Customer_ID", "Order_Date"])
    )
else:
    problematic_customer_ids = pd.DataFrame(
        columns=df.columns
    )

problematic_customer_ids.to_excel(
    REPORT_DIR / "Problematic_Customer_Profiles.xlsx",
    index=False
)

# ==================================================
# Final status
# ==================================================

checks = {
    "Duplicate rows": duplicate_rows == 0,
    "Invalid dates": df["Order_Date"].isna().sum() == 0,
    "Zero quantity": zero_quantity == 0,
    "Negative quantity": negative_quantity == 0,
    "Zero unit price": zero_price == 0,
    "Negative unit price": negative_price == 0,
    "Incorrect sales calculations": incorrect_sales == 0,
    "Order ID integrity": len(invalid_orders) == 0,
    "Customer profile consistency": len(inconsistent_customers) == 0
}

print("\nFINAL CHECK STATUS")
print("=" * 50)

for check, passed in checks.items():
    print(
        f"{check}: {'PASS' if passed else 'CHECK'}"
    )

print("\nReports saved to:")
print(REPORT_DIR)
print("\nData-quality check completed successfully.")
