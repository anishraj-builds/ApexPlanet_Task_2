# Data Dictionary

## 1. Dataset Information

Dataset: ApexPlanet Data Analytics Dataset

Total transaction records: 1,000

Total original columns: 12

Unique customers: 947

Distinct Order IDs: 992

Total units sold: 5,435

Total revenue: ₹139,399,439.65

Each row represents one transaction record from the source dataset.

## 2. Column Definitions

| Column        | Description                                                   | Data Type   | Example       | Data Quality                                                               |
| ------------- | ------------------------------------------------------------- | ----------- | ------------- | -------------------------------------------------------------------------- |
| Order_ID      | Source order identifier assigned to an order                  | Text        | ORD100001     | One problematic ID, ORD100050, appears across multiple customers and dates |
| Order_Date    | Date on which the transaction occurred                        | Date        | 2025-01-15    | No invalid dates found                                                     |
| Customer_ID   | Unique customer identifier                                    | Text        | CUST1001      | 947 unique customers                                                       |
| Customer_Name | Name associated with the customer record                      | Text        | Customer Name | Used for customer-level identification                                     |
| Age           | Age of the customer                                           | Integer     | 25            | 20 missing values                                                          |
| Gender        | Gender recorded for the customer                              | Categorical | Male          | Used for gender-based analysis                                             |
| City          | Customer city                                                 | Categorical | Bengaluru     | 13 missing values                                                          |
| Product       | Product purchased in the transaction                          | Categorical | Laptop        | Used for product performance analysis                                      |
| Category      | Category assigned to the purchased product                    | Categorical | Electronics   | Five categories are present                                                |
| Quantity      | Number of units purchased                                     | Integer     | 2             | No zero or negative quantities found                                       |
| Unit_Price    | Price of one unit in the transaction                          | Numeric     | 45000.00      | No zero or negative prices found                                           |
| Total_Sales   | Total transaction value calculated from Quantity × Unit_Price | Numeric     | 90000.00      | 0 incorrect sales calculations                                             |

## 3. Data Grain

Each row represents one transaction record.

The dataset contains 1,000 transaction records.

Transaction-level calculations use all 1,000 source records.

## 4. Identifier Information

### Order_ID

Order_ID represents the source order identifier.

The dataset contains 992 distinct Order IDs across 1,000 transaction records.

ORD100050 appears across multiple records with different customers and dates.

Because of this source-data issue, Order_ID is not treated as a fully unique transaction identifier.

### Customer_ID

Customer_ID identifies the customer associated with a transaction.

The dataset contains 947 customers.

### Transaction_ID

Transaction_ID is used by the analytical database as the preferred transaction-level identifier.

It provides a unique identifier for individual transaction records.

## 5. Data Types Used in Analysis

Text fields:

* Order_ID
* Customer_ID
* Customer_Name
* Gender
* City
* Product
* Category

Date field:

* Order_Date

Integer fields:

* Age
* Quantity

Numeric fields:

* Unit_Price
* Total_Sales

## 6. Missing Data

The data-quality analysis identified:

* Age: 20 missing values
* City: 13 missing values

No missing values were identified as a reason to remove transaction records.

## 7. Validation Rules

The following validation checks were performed:

* Duplicate row check
* Missing-value check
* Date validation
* Quantity validation
* Unit price validation
* Total sales calculation validation
* Order_ID integrity check

Results:

* Duplicate rows: 0
* Invalid dates: 0
* Zero quantities: 0
* Negative quantities: 0
* Zero prices: 0
* Negative prices: 0
* Incorrect Total_Sales calculations: 0
* Problematic Order IDs: 1

## 8. Derived Fields Used in Analysis

The analysis also creates derived fields for analytical purposes.

### Month

Created from Order_Date to analyze monthly revenue.

Example:

2025-03

### Age_Group

Customers are grouped into:

* 18-24
* 25-34
* 35-44
* 45-54
* 55-65

### MoM_Growth_Percent

Month-over-month revenue growth is calculated as the percentage change in monthly revenue compared with the previous month.

### Customer Type

Customers are classified based on distinct Order ID count.

One-Time Customer:

One distinct Order ID.

Repeat Customer:

More than one distinct Order ID.

## 9. Important Analytical Definitions

### Total Revenue

Sum of Total_Sales across all 1,000 transaction records.

Total Revenue:

₹139,399,439.65

### Transactions

Number of source transaction records.

Transactions:

1,000

### Distinct Order IDs

Number of unique Order_ID values.

Distinct Order IDs:

992

### Average Transaction Value

Total Revenue divided by the number of transaction records.

Average Transaction Value:

₹139,399.44

### Repeat Customer Rate

Number of repeat customers divided by total customers.

Repeat Customer Rate:

5.49%

## 10. Data Period

The dataset contains transactions from 2025 and January 2026.

January 2026 is treated as a partial period.

Complete-month comparisons therefore focus on the available complete months, while January 2026 is reported separately.

## 11. Data Quality Limitation

The main identifier issue is the repeated Order_ID value ORD100050.

The record was retained because removing source records without evidence would change the dataset.

The issue is documented in:

`report/Problematic_Order_IDs.xlsx`

The broader customer-profile inconsistencies are documented in:

`report/Problematic_Customer_Profiles.xlsx`
