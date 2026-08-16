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
# Read and prepare dataset
# ==================================================

df = pd.read_excel(file)

df["City"] = df["City"].fillna("Unknown")

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# ==================================================
# Numerical statistics
# ==================================================

num_cols = [
    "Age",
    "Quantity",
    "Unit_Price",
    "Total_Sales"
]

print("DESCRIPTIVE STATISTICS")
print("=" * 50)

numeric_stats = (
    df[num_cols]
    .describe()
    .round(2)
)

print(numeric_stats)

# ==================================================
# Median and mode
# ==================================================

median = df[num_cols].median().round(2)

print("\nMEDIAN")
print("=" * 50)
print(median)

mode_rows = []

for col in num_cols:
    mode_values = df[col].mode(dropna=True)

    mode_rows.append({
        "Column": col,
        "Mode": mode_values.iloc[0]
        if len(mode_values) > 0
        else None
    })

mode_summary = pd.DataFrame(mode_rows)

print("\nMODE")
print("=" * 50)
print(mode_summary)

# ==================================================
# Categorical analysis
# ==================================================

cat_cols = [
    "Gender",
    "City",
    "Product",
    "Category"
]

print("\nCATEGORICAL ANALYSIS")
print("=" * 50)

categorical_summaries = {}

for col in cat_cols:
    counts = df[col].value_counts(dropna=False)
    percentages = (
        df[col]
        .value_counts(dropna=False, normalize=True)
        .mul(100)
        .round(2)
    )

    categorical_summaries[col] = pd.DataFrame({
        "Count": counts,
        "Percentage": percentages
    })

    print("\n", col)
    print(categorical_summaries[col])

# ==================================================
# Revenue by Category
# ==================================================

category_sales = (
    df.groupby("Category")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

category_share = (
    category_sales
    / df["Total_Sales"].sum()
    * 100
)

category_summary = pd.DataFrame({
    "Revenue": category_sales.round(2),
    "Revenue_Share_Percent": category_share.round(2)
})

print("\nCATEGORY REVENUE SHARE")
print("=" * 50)
print(category_summary)

# ==================================================
# Revenue by Product and Pareto analysis
# ==================================================

product_sales = (
    df.groupby("Product")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

product_share = (
    product_sales
    / df["Total_Sales"].sum()
    * 100
)

product_summary = pd.DataFrame({
    "Revenue": product_sales.round(2),
    "Revenue_Share_Percent": product_share.round(2)
})

product_pareto = product_summary.copy()
product_pareto["Cumulative_Revenue_Percent"] = (
    product_pareto["Revenue_Share_Percent"]
    .cumsum()
    .round(2)
)

print("\nREVENUE BY PRODUCT")
print("=" * 50)
print(product_pareto)

# ==================================================
# Monthly Revenue Analysis
# ==================================================

df["Month"] = df["Order_Date"].dt.to_period("M")

monthly_summary = (
    df.groupby("Month")
    .agg(
        Revenue=("Total_Sales", "sum"),
        Transactions=("Total_Sales", "size"),
        Distinct_Order_IDs=("Order_ID", "nunique"),
        Units=("Quantity", "sum")
    )
)

monthly_summary["Average_Transaction_Value"] = (
    monthly_summary["Revenue"]
    / monthly_summary["Transactions"]
)

monthly_summary["Revenue_MoM_Growth_Percent"] = (
    monthly_summary["Revenue"]
    .pct_change()
    .mul(100)
)

print("\nMONTHLY PERFORMANCE")
print("=" * 50)
print(monthly_summary.round(2))

# ==================================================
# Age-group analysis
# ==================================================

age_bins = [17, 24, 34, 44, 54, 65]
age_labels = [
    "18-24",
    "25-34",
    "35-44",
    "45-54",
    "55-65"
]

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=age_bins,
    labels=age_labels
)

age_summary = (
    df.groupby("Age_Group", observed=True)
    .agg(
        Transactions=("Total_Sales", "size"),
        Revenue=("Total_Sales", "sum"),
        Average_Transaction=("Total_Sales", "mean")
    )
    .round(2)
)

print("\nAGE GROUP PERFORMANCE")
print("=" * 50)
print(age_summary)

# ==================================================
# Gender performance
# ==================================================

gender_summary = (
    df.groupby("Gender")
    .agg(
        Transactions=("Total_Sales", "size"),
        Revenue=("Total_Sales", "sum"),
        Average_Transaction=("Total_Sales", "mean")
    )
    .round(2)
)

print("\nGENDER PERFORMANCE")
print("=" * 50)
print(gender_summary)

# ==================================================
# Category revenue per unit
# ==================================================

category_unit_summary = (
    df.groupby("Category")
    .agg(
        Units_Sold=("Quantity", "sum"),
        Revenue=("Total_Sales", "sum")
    )
)

category_unit_summary["Revenue_Per_Unit"] = (
    category_unit_summary["Revenue"]
    / category_unit_summary["Units_Sold"]
)

category_unit_summary = category_unit_summary.round(2)

print("\nCATEGORY REVENUE PER UNIT")
print("=" * 50)
print(category_unit_summary.sort_values(
    "Revenue_Per_Unit",
    ascending=False
))

# ==================================================
# Overall KPI Summary
# ==================================================

total_revenue = df["Total_Sales"].sum()
total_transactions = len(df)
distinct_order_ids = df["Order_ID"].nunique()
total_customers = df["Customer_ID"].nunique()
total_units = df["Quantity"].sum()

average_transaction_value = (
    total_revenue
    / total_transactions
)

repeat_customers = (
    df.groupby("Customer_ID")["Order_ID"]
    .nunique()
)

repeat_customer_count = (
    repeat_customers > 1
).sum()

repeat_customer_rate = (
    repeat_customer_count
    / total_customers
    * 100
)

# ==================================================
# Complete-month identification
# ==================================================

max_date = df["Order_Date"].max()
last_month = max_date.to_period("M")

complete_months = monthly_summary.index[
    monthly_summary.index < last_month
]

if len(complete_months) > 0:
    strongest_complete_month = monthly_summary.loc[
        complete_months,
        "Revenue"
    ].idxmax()

    weakest_complete_month = monthly_summary.loc[
        complete_months,
        "Revenue"
    ].idxmin()
else:
    strongest_complete_month = None
    weakest_complete_month = None

print("\nOVERALL KPIs")
print("=" * 50)
print("Total Revenue:", round(total_revenue, 2))
print("Transactions:", total_transactions)
print("Distinct Order IDs:", distinct_order_ids)
print("Total Customers:", total_customers)
print("Total Units:", total_units)
print(
    "Average Transaction Value:",
    round(average_transaction_value, 2)
)
print("Repeat Customers:", repeat_customer_count)
print(
    "Repeat Customer Rate:",
    round(repeat_customer_rate, 2),
    "%"
)

if strongest_complete_month is not None:
    print(
        "Strongest Complete Month:",
        strongest_complete_month,
        round(
            monthly_summary.loc[
                strongest_complete_month,
                "Revenue"
            ],
            2
        )
    )

    print(
        "Weakest Complete Month:",
        weakest_complete_month,
        round(
            monthly_summary.loc[
                weakest_complete_month,
                "Revenue"
            ],
            2
        )
    )

# ==================================================
# Top 5 Products
# ==================================================

print("\nTOP 5 PRODUCTS BY REVENUE")
print("=" * 50)
print(product_sales.head(5).round(2))

# ==================================================
# Save analysis workbook
# ==================================================

kpi_summary = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Transactions",
        "Distinct Order IDs",
        "Customers",
        "Units Sold",
        "Average Transaction Value",
        "Repeat Customers",
        "Repeat Customer Rate Percent"
    ],
    "Value": [
        total_revenue,
        total_transactions,
        distinct_order_ids,
        total_customers,
        total_units,
        average_transaction_value,
        repeat_customer_count,
        repeat_customer_rate
    ]
})

stats_file = REPORT_DIR / "Stats_Summary.xlsx"

with pd.ExcelWriter(stats_file, engine="openpyxl") as writer:
    kpi_summary.to_excel(
        writer,
        sheet_name="KPIs",
        index=False
    )

    category_summary.to_excel(
        writer,
        sheet_name="Category",
        index=True
    )

    product_pareto.to_excel(
        writer,
        sheet_name="Product_Pareto",
        index=True
    )

    monthly_summary.to_excel(
        writer,
        sheet_name="Monthly",
        index=True
    )

    age_summary.to_excel(
        writer,
        sheet_name="Age_Groups",
        index=True
    )

    gender_summary.to_excel(
        writer,
        sheet_name="Gender",
        index=True
    )

    category_unit_summary.to_excel(
        writer,
        sheet_name="Category_Unit",
        index=True
    )

print("\nDATA SUMMARY")
print("=" * 50)
print("Rows:", len(df))
print("Columns:", len(df.columns))
print(
    "Date Range:",
    df["Order_Date"].min().date(),
    "to",
    df["Order_Date"].max().date()
)
print("\nStatistics analysis completed successfully.")
print("Stats workbook saved to:")
print(stats_file)
