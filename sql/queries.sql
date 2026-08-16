-- ============================================================
-- ApexPlanet Task-2
-- SQL Business Analysis
-- Database: SQLite
--
-- Final submission contains 7 specific business questions,
-- matching the assignment requirement of 5-7 questions.
-- The queries demonstrate filtering, aggregation, and multi-table joins.
-- There are 1,000 transactions and 992 distinct Order_IDs.
-- ORD100050 is repeated across multiple customers and dates.
-- January 2026 is a partial period.
-- ============================================================


-- ============================================================
-- Q1: What are the top 5 products by revenue?
-- Uses a multi-table join between sales and products.
-- ============================================================

SELECT
    p.Product,
    p.Category,
    SUM(s.Quantity) AS Units_Sold,
    ROUND(SUM(s.Total_Sales), 2) AS Revenue,
    ROUND(
        SUM(s.Total_Sales) / SUM(s.Quantity),
        2
    ) AS Revenue_Per_Unit
FROM sales s
JOIN products p
    ON s.Product = p.Product
GROUP BY p.Product, p.Category
ORDER BY Revenue DESC
LIMIT 5;


-- ============================================================
-- Q2: What is the monthly revenue, transaction count,
-- distinct order count, units sold, and average transaction value?
-- January 2026 is a partial period.
-- ============================================================

SELECT
    strftime('%Y-%m', Order_Date) AS Month,
    COUNT(*) AS Transactions,
    COUNT(DISTINCT Order_ID) AS Distinct_Order_IDs,
    SUM(Quantity) AS Units,
    ROUND(SUM(Total_Sales), 2) AS Revenue,
    ROUND(
        SUM(Total_Sales) / COUNT(*),
        2
    ) AS Average_Transaction_Value
FROM sales
GROUP BY Month
ORDER BY Month;


-- ============================================================
-- Q3: Which city-category combinations generate the most revenue?
-- ============================================================

SELECT
    COALESCE(City, 'Unknown') AS City,
    Category,
    ROUND(SUM(Total_Sales), 2) AS Revenue,
    SUM(Quantity) AS Units_Sold
FROM sales
GROUP BY
    COALESCE(City, 'Unknown'),
    Category
ORDER BY Revenue DESC;


-- ============================================================
-- Q4: Which customers placed more than one distinct order?
-- Uses a multi-table join between sales and customers.
-- ============================================================

SELECT
    c.Customer_ID,
    c.Customer_Name,
    COUNT(DISTINCT s.Order_ID) AS Distinct_Orders,
    ROUND(SUM(s.Total_Sales), 2) AS Revenue
FROM sales s
JOIN customers c
    ON s.Customer_ID = c.Customer_ID
GROUP BY c.Customer_ID, c.Customer_Name
HAVING COUNT(DISTINCT s.Order_ID) > 1
ORDER BY Distinct_Orders DESC, Revenue DESC;


-- ============================================================
-- Q5: How does revenue and average transaction value differ by gender?
-- ============================================================

SELECT
    COALESCE(Gender, 'Unknown') AS Gender,
    COUNT(*) AS Transactions,
    COUNT(DISTINCT Order_ID) AS Distinct_Order_IDs,
    ROUND(SUM(Total_Sales), 2) AS Revenue,
    ROUND(
        SUM(Total_Sales) / COUNT(*),
        2
    ) AS Average_Transaction_Value
FROM sales
GROUP BY COALESCE(Gender, 'Unknown')
ORDER BY Average_Transaction_Value DESC;


-- ============================================================
-- Q6: How does revenue and average transaction value differ
-- across customer age groups?
-- Missing Age values are retained as Unknown.
-- ============================================================

SELECT
    CASE
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Age BETWEEN 55 AND 65 THEN '55-65'
        ELSE 'Unknown'
    END AS Age_Group,
    COUNT(*) AS Transactions,
    COUNT(DISTINCT Order_ID) AS Distinct_Order_IDs,
    ROUND(SUM(Total_Sales), 2) AS Revenue,
    ROUND(
        SUM(Total_Sales) / COUNT(*),
        2
    ) AS Average_Transaction_Value
FROM sales
GROUP BY Age_Group
ORDER BY Revenue DESC;


-- ============================================================
-- Q7: Which transactions have sales above ₹400,000?
-- Uses a multi-table join between sales and orders.
-- ============================================================

SELECT
    s.Transaction_ID,
    s.Order_ID,
    s.Customer_ID,
    s.Product,
    s.Category,
    ROUND(s.Total_Sales, 2) AS Total_Sales,
    o.Order_ID_Status
FROM sales s
JOIN orders o
    ON s.Order_ID = o.Order_ID
WHERE s.Total_Sales > 400000
ORDER BY s.Total_Sales DESC;