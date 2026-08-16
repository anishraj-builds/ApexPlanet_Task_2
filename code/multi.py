import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

# ==================================================
# Project paths
# ==================================================

BASE = Path(__file__).resolve().parent.parent
OUTPUT = BASE / "report" / "charts"
OUTPUT.mkdir(parents=True, exist_ok=True)

file = BASE / "ApexPlanet_DataAnalytics_Dataset.xlsx"

df = pd.read_excel(file)

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# ==================================================
# Numerical columns
# ==================================================

num_cols = [
    "Age",
    "Quantity",
    "Unit_Price",
    "Total_Sales"
]

missing_cols = [
    col for col in num_cols
    if col not in df.columns
]

if missing_cols:
    raise ValueError(
        f"Missing required columns: {missing_cols}"
    )

# ==================================================
# 1. Quantity vs Total Sales
# ==================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Quantity",
    y="Total_Sales"
)

plt.title("Quantity vs Total Sales")
plt.xlabel("Quantity")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(
    OUTPUT / "quantity_sales.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==================================================
# 2. Unit Price vs Total Sales
# ==================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="Unit_Price",
    y="Total_Sales"
)

plt.title("Unit Price vs Total Sales")
plt.xlabel("Unit Price")
plt.ylabel("Total Sales")
plt.tight_layout()
plt.savefig(
    OUTPUT / "price_sales.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==================================================
# 3. Correlation Heatmap
# ==================================================

corr = df[num_cols].corr()

print("\nCORRELATION MATRIX")
print("=" * 50)
print(corr.round(2))

sales_corr = (
    corr["Total_Sales"]
    .drop("Total_Sales")
    .sort_values(ascending=False)
)

print("\nCORRELATION WITH TOTAL SALES")
print("=" * 50)
print(sales_corr.round(2))

plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(
    OUTPUT / "heatmap.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==================================================
# 4. Pair Plot
# Uses pandas scatter_matrix for broader matplotlib
# compatibility across Python and seaborn versions.
# ==================================================

pair_data = df[num_cols].dropna()

from pandas.plotting import scatter_matrix

axes = scatter_matrix(
    pair_data,
    figsize=(10, 10),
    diagonal="hist",
    alpha=0.6
)

for ax in axes.ravel():
    ax.tick_params(axis="both", labelsize=7)

plt.suptitle(
    "Pair Plot of Numerical Variables",
    y=0.98
)
plt.tight_layout()
plt.savefig(
    OUTPUT / "pairplot.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ==================================================
# 5. Revenue vs Quantity and Unit Price Summary
# ==================================================

summary = pd.DataFrame({
    "Correlation_with_Total_Sales": sales_corr.round(4)
})

summary.to_excel(
    BASE / "report" / "Multivariate_Correlation_Summary.xlsx"
)

# ==================================================
# Final Summary
# ==================================================

print("\nMULTIVARIATE ANALYSIS SUMMARY")
print("=" * 50)

for variable, value in sales_corr.items():
    print(
        f"{variable} vs Total_Sales: {value:.2f}"
    )

print("\nCharts saved to:")
print(OUTPUT)
print("\nCorrelation summary saved to:")
print(BASE / "report" / "Multivariate_Correlation_Summary.xlsx")
print("\nAll multivariate analysis completed successfully.")
