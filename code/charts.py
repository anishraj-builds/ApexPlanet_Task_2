import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# ==================================================
# Project paths
# ==================================================

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "report" / "charts"
OUTPUT.mkdir(parents=True, exist_ok=True)

file = BASE / "ApexPlanet_DataAnalytics_Dataset.xlsx"

df = pd.read_excel(file)

# Convert date safely
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Handle missing city values for geographic analysis
df["City"] = df["City"].fillna("Unknown")

# ==================================================
# Helper function
# ==================================================

def save_chart(filename):
    plt.tight_layout()
    plt.savefig(
        OUTPUT / filename,
        dpi=300,
        bbox_inches="tight"
    )
    plt.close()


# ==================================================
# 1. Age Distribution
# ==================================================

plt.figure(figsize=(8, 5))
plt.hist(df["Age"].dropna(), bins=10)
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Number of Transactions")
save_chart("age.png")


# ==================================================
# 2. Quantity Distribution
# ==================================================

plt.figure(figsize=(8, 5))
plt.hist(df["Quantity"].dropna(), bins=10)
plt.title("Quantity Distribution")
plt.xlabel("Quantity")
plt.ylabel("Number of Transactions")
save_chart("quantity.png")


# ==================================================
# 3. Total Sales Distribution
# ==================================================

plt.figure(figsize=(8, 5))
plt.hist(df["Total_Sales"].dropna(), bins=20)
plt.title("Total Sales Distribution")
plt.xlabel("Total Sales")
plt.ylabel("Number of Transactions")
save_chart("sales.png")


# ==================================================
# 4. Transactions by Gender
# ==================================================

gender_transactions = (
    df.groupby("Gender")
    .size()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
gender_transactions.plot(kind="bar")
plt.title("Transactions by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=0)
save_chart("gender.png")


# ==================================================
# 5. Revenue by Category
# ==================================================

category = (
    df.groupby("Category")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
category.plot(kind="bar")
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45, ha="right")
save_chart("category.png")


# ==================================================
# 6. Revenue by City
# ==================================================

city = (
    df.groupby("City")["Total_Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
city.plot(kind="bar")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45, ha="right")
save_chart("city.png")


# ==================================================
# 7. Monthly Revenue
# ==================================================

df["Month"] = df["Order_Date"].dt.to_period("M")

monthly = (
    df.groupby("Month")["Total_Sales"]
    .sum()
)

plt.figure(figsize=(10, 5))
monthly.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
save_chart("monthly.png")


# ==================================================
# 8. Month-over-Month Revenue Growth
# ==================================================

monthly_growth = monthly.pct_change().mul(100)

plt.figure(figsize=(10, 5))
monthly_growth.plot(kind="bar")
plt.title("Month-over-Month Revenue Growth")
plt.xlabel("Month")
plt.ylabel("Growth (%)")
plt.xticks(rotation=45)
plt.axhline(y=0, linewidth=1)
save_chart("monthly_growth.png")


# ==================================================
# 9. Revenue by Age Group
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

age_revenue = (
    df.groupby("Age_Group", observed=True)["Total_Sales"]
    .sum()
)

plt.figure(figsize=(8, 5))
age_revenue.plot(kind="bar")
plt.title("Revenue by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Total Revenue")
plt.xticks(rotation=0)
save_chart("age_group_revenue.png")


# ==================================================
# 10. Revenue per Unit by Category
# ==================================================

category_unit = (
    df.groupby("Category")
    .agg(
        Revenue=("Total_Sales", "sum"),
        Units_Sold=("Quantity", "sum")
    )
)

category_unit["Revenue_Per_Unit"] = (
    category_unit["Revenue"]
    / category_unit["Units_Sold"]
)

category_unit = category_unit["Revenue_Per_Unit"].sort_values(ascending=False)

plt.figure(figsize=(8, 5))
category_unit.plot(kind="bar")
plt.title("Revenue per Unit by Category")
plt.xlabel("Category")
plt.ylabel("Revenue per Unit")
plt.xticks(rotation=45, ha="right")
save_chart("category_revenue_per_unit.png")


# ==================================================
# Final Summary
# ==================================================

print("\nCHART SUMMARY")
print("=" * 50)

for chart in [
    "age.png",
    "quantity.png",
    "sales.png",
    "gender.png",
    "category.png",
    "city.png",
    "monthly.png",
    "monthly_growth.png",
    "age_group_revenue.png",
    "category_revenue_per_unit.png"
]:
    print(chart)

print("\nCharts saved to:")
print(OUTPUT)
print("\nAll charts created successfully.")
