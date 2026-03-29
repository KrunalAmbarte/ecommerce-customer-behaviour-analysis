-- Query 1: Top 10 Countries by Revenue
SELECT Country,
       ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
       COUNT(DISTINCT "Customer ID") AS Unique_Customers
FROM transactions
GROUP BY Country
ORDER BY Total_Revenue DESC
LIMIT 10;

-- Query 2: Monthly Revenue Trend
SELECT STRFTIME('%Y-%m', InvoiceDate) AS Month,
       ROUND(SUM(TotalPrice), 2) AS Monthly_Revenue,
       COUNT(DISTINCT Invoice) AS Total_Orders
FROM transactions
GROUP BY Month
ORDER BY Month;

-- Query 3: Revenue by Customer Segment
SELECT Segment,
       COUNT("Customer ID") AS Customer_Count,
       ROUND(AVG(Monetary), 2) AS Avg_Monetary,
       ROUND(SUM(Monetary), 2) AS Total_Revenue
FROM rfm
GROUP BY Segment
ORDER BY Total_Revenue DESC;

-- Query 4: Top 10 Customers by Revenue
SELECT "Customer ID",
       COUNT(DISTINCT Invoice) AS Total_Orders,
       ROUND(SUM(TotalPrice), 2) AS Total_Revenue
FROM transactions
GROUP BY "Customer ID"
ORDER BY Total_Revenue DESC
LIMIT 10;

-- Query 5: Top 10 Best Selling Products
SELECT Description,
       SUM(Quantity) AS Total_Quantity_Sold,
       ROUND(SUM(TotalPrice), 2) AS Total_Revenue
FROM transactions
GROUP BY Description
ORDER BY Total_Quantity_Sold DESC
LIMIT 10;