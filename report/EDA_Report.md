# Exploratory Data Analysis Report

## 1. Project Overview

This project analyzes customer transaction data to identify revenue patterns, product performance, category performance, customer segments, geographic trends, monthly sales behavior, and customer retention opportunities.

The analysis uses Python, Pandas, Matplotlib, Seaborn, SQLite, SQL, Excel, and PowerPoint.

## 2. Dataset Overview

The dataset contains 1,000 transaction records and 12 original columns.

The analysis covers transaction, customer, product, pricing, quantity, location, and sales information.

The available period contains 2025 transactions and January 2026 transactions. January 2026 is treated as a partial period.

## 3. KPI Snapshot

| KPI                       |           Value |
| ------------------------- | --------------: |
| Total Revenue             | ₹139,399,439.65 |
| Transactions              |           1,000 |
| Distinct Order IDs        |             992 |
| Customers                 |             947 |
| Units Sold                |           5,435 |
| Average Transaction Value |     ₹139,399.44 |
| Median Transaction Value  |     ₹108,594.02 |
| Repeat Customers          |              52 |
| Repeat Customer Rate      |           5.49% |

## 4. Data Quality Assessment

The dataset was checked for missing values, duplicate records, invalid dates, invalid quantities, invalid prices, and incorrect sales calculations.

The following findings were identified:

| Check                              | Result |
| ---------------------------------- | -----: |
| Total Records                      |  1,000 |
| Missing Age Values                 |     20 |
| Missing City Values                |     13 |
| Duplicate Rows                     |      0 |
| Invalid Dates                      |      0 |
| Zero Quantity Records              |      0 |
| Negative Quantity Records          |      0 |
| Zero Unit Price Records            |      0 |
| Negative Unit Price Records        |      0 |
| Incorrect Total Sales Calculations |      0 |
| Problematic Order IDs              |      1 |

## 5. Order ID Integrity Issue

The dataset contains 1,000 transaction records and 992 distinct Order IDs.

ORD100050 appears across multiple records with different customers and dates.

Therefore, transaction-level analysis uses all 1,000 source records, while distinct Order IDs are reported separately.

This issue was retained as a documented source-data quality finding instead of removing records without evidence.

Transaction_ID should be used when unique transaction-level identification is required.

## 6. Descriptive Analysis

The analysis calculated revenue, quantity, transaction counts, customer counts, averages, medians, and categorical distributions.

Total revenue is ₹139,399,439.65 from 1,000 transaction records.

The average transaction value is ₹139,399.44.

The median transaction value is ₹108,594.02.

The difference between average and median transaction value indicates that higher-value transactions influence the average.

## 7. Category Performance

Electronics is the leading revenue-generating category.

Electronics generated ₹50,778,581.70, representing 36.43% of total revenue.

The remaining categories are Education, Grocery, Furniture, and Fashion.

Category performance was compared using total revenue, units sold, and revenue per unit.

## 8. Product Performance

Product-level analysis was used to identify the highest revenue-generating products.

Laptop is the leading product with revenue of ₹25,443,008.51.

Mobile is another major revenue-generating product with revenue of ₹25,335,573.19.

A Pareto analysis was also performed to identify the cumulative contribution of products to total revenue.

## 9. Monthly Performance

Monthly revenue was analyzed to identify changes in sales performance.

March 2025 recorded the highest complete-month revenue at ₹13,059,899.94 across 89 transactions.

September 2025 recorded the lowest complete-month revenue at ₹9,179,896.29.

Month-over-month revenue growth was also calculated to identify periods of increase and decline.

January 2026 is treated as a partial period and is not compared directly with complete months.

## 10. Customer Analysis

Customer analysis examined customer count, gender, age groups, and repeat purchasing behavior.

The dataset contains 947 customers.

52 customers have more than one distinct Order ID.

This gives a repeat customer rate of 5.49%.

The remaining 895 customers are classified as one-time customers under the distinct Order ID method.

Customer type analysis is based on distinct Order ID count.

## 11. Geographic Analysis

City-level revenue was analyzed to identify the strongest geographic markets.

Patna is the highest-revenue city with revenue of ₹19,285,966.89.

The top cities were compared using total revenue to identify locations with stronger sales performance.

## 12. Gender Analysis

Revenue and average transaction value were compared across gender groups.

The analysis provides a view of customer contribution and transaction behavior by gender.

The results are available in the generated Stats_Summary.xlsx file.

## 13. Age Group Analysis

Customers were grouped into the following age ranges:

18-24

25-34

35-44

45-54

55-65

Revenue, transaction count, and average transaction value were compared across these groups.

## 14. SQL Business Analysis

SQLite was used to answer 7 specific business questions.

The SQL analysis covers:

1. Top products by revenue.
2. Monthly revenue performance.
3. City and category revenue.
4. Repeat customer analysis.
5. Gender performance.
6. Age-group performance.
7. High-value transactions.

The SQL analysis demonstrates filtering, aggregation, grouping, ordering, and multi-table joins.

The SQL results are stored in SQL_Results.xlsx.

The SQLite database is stored as sales.db.

## 15. Multivariate Analysis

Correlation and multivariate analysis were performed to examine relationships between numerical variables.

The analysis includes:

Quantity.

Unit Price.

Total Sales.

Age.

The correlation heatmap and pairplot are available in the report charts folder.

## 16. Key Business Insights

1. Electronics is the leading category and contributes 36.43% of total revenue.

2. Laptop and Mobile are the two major revenue-generating products.

3. Patna is the highest-revenue city.

4. March 2025 is the strongest complete month.

5. Repeat customers represent 5.49% of customers.

6. The dataset contains a documented Order_ID integrity issue involving ORD100050.

## 17. Business Recommendations

1. Maintain strong inventory availability for high-revenue Electronics products.

2. Use Laptop and Mobile purchases for cross-selling opportunities.

3. Investigate the revenue decline observed around September 2025.

4. Target one-time customers with repeat-purchase campaigns.

5. Analyze high-performing cities to develop location-specific sales strategies.

6. Review the source-system handling of Order_ID values to prevent repeated identifiers across unrelated transactions.

## 18. Limitations

The analysis is based on the supplied dataset.

The dataset contains missing Age and City values.

The dataset contains a documented Order_ID uniqueness issue.

January 2026 represents a partial period.

The analysis describes patterns within the supplied data and does not establish external causes for the observed sales patterns.

## 19. Project Workflow

The complete analytical workflow is:

Dataset → Data Quality → EDA → SQL → Visualization → Business Insights → Dashboard

Python was used for data validation, descriptive analysis, visualization, and multivariate analysis.

SQLite and SQL were used for structured business analysis.

PowerPoint was used to present the final business findings.

## 20. Conclusion

The analysis provides a structured view of revenue, products, categories, customers, cities, and monthly sales performance.

The strongest revenue contribution comes from Electronics.

Laptop and Mobile are major product contributors.

Patna is the leading city by revenue.

Customer retention remains an area for further business focus because repeat customers account for 5.49% of customers.

The project combines data-quality validation, Python analysis, SQL analysis, visualization, and business recommendations into one reproducible analytics workflow.
