# import pandas as pd
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import sqlite3


# df = pd.read_excel('online_retail_II.xlsx', sheet_name='Year 2009-2010')
# print(df.shape)
# print(df.dtypes)
# print(df.isnull().sum())
# print(df.head())
# print(df['Country'].nunique())
# print(df['InvoiceDate'].min(), df['InvoiceDate'].max())

# ----------------------------------------------------------------------

# Data Cleaning

# # ── Load Data ──────────────────────────────────────────
# df = pd.read_csv('online_retail_II.csv')
# print("Original shape:", df.shape)

# # ── Step 1: Drop missing Customer IDs ──────────────────
# df = df.dropna(subset=['Customer ID'])
# print("After dropping missing Customer ID:", df.shape)

# # ── Step 2: Drop missing Descriptions ──────────────────
# df = df.dropna(subset=['Description'])
# print("After dropping missing Description:", df.shape)

# # ── Step 3: Remove negative Quantities (returns) ───────
# df = df[df['Quantity'] > 0]
# print("After removing negative Quantity:", df.shape)

# # ── Step 4: Remove negative/zero Prices ────────────────
# df = df[df['Price'] > 0]
# print("After removing negative Price:", df.shape)

# # ── Step 5: Remove duplicate rows ──────────────────────
# df = df.drop_duplicates()
# print("After removing duplicates:", df.shape)

# # ── Step 6: Fix data types ──────────────────────────────
# df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
# df['Customer ID'] = df['Customer ID'].astype(int)
# print("\nData types after fixing:")
# print(df.dtypes)

# # ── Step 7: Create TotalPrice column ───────────────────
# df['TotalPrice'] = df['Quantity'] * df['Price']

# # ── Step 8: Final check ─────────────────────────────────
# print("\nFinal shape:", df.shape)
# print("\nMissing values after cleaning:")
# print(df.isnull().sum())
# print("\nSample cleaned data:")
# print(df.head())

# # ── Step 9: Save cleaned data ───────────────────────────
# df.to_csv('online_retail_cleaned.csv', index=False)
# print("\nCleaned file saved as online_retail_cleaned.csv")

# ----------------------------------------------------------------------

# Exploratory Data Analysis (EDA)

# # ── Load cleaned data ───────────────────────────────────
# df = pd.read_csv('online_retail_cleaned.csv')
# df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# print("Data loaded. Shape:", df.shape)

# # ── EDA 1: Revenue by Country ───────────────────────────
# country_revenue = df.groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).head(10)
# print("\nTop 10 Countries by Revenue:")
# print(country_revenue)

# plt.figure(figsize=(12,5))
# country_revenue.plot(kind='bar', color='steelblue')
# plt.title('Top 10 Countries by Revenue')
# plt.xlabel('Country')
# plt.ylabel('Total Revenue')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('revenue_by_country.png')
# plt.show()
# print("Saved: revenue_by_country.png")

# # ── EDA 2: Monthly Revenue Trend ───────────────────────
# df['Month'] = df['InvoiceDate'].dt.to_period('M')
# monthly_revenue = df.groupby('Month')['TotalPrice'].sum()
# print("\nMonthly Revenue:")
# print(monthly_revenue)

# plt.figure(figsize=(12,5))
# monthly_revenue.plot(kind='line', marker='o', color='darkorange')
# plt.title('Monthly Revenue Trend')
# plt.xlabel('Month')
# plt.ylabel('Total Revenue')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('monthly_revenue_trend.png')
# plt.show()
# print("Saved: monthly_revenue_trend.png")

# # ── EDA 3: Top 10 Customers by Spend ───────────────────
# top_customers = df.groupby('Customer ID')['TotalPrice'].sum().sort_values(ascending=False).head(10)
# print("\nTop 10 Customers by Total Spend:")
# print(top_customers)

# plt.figure(figsize=(12,5))
# top_customers.plot(kind='bar', color='seagreen')
# plt.title('Top 10 Customers by Total Spend')
# plt.xlabel('Customer ID')
# plt.ylabel('Total Spend')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('top_customers.png')
# plt.show()
# print("Saved: top_customers.png")

# # ── EDA 4: Top 10 Products by Quantity Sold ────────────
# top_products = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
# print("\nTop 10 Products by Quantity Sold:")
# print(top_products)

# plt.figure(figsize=(12,5))
# top_products.plot(kind='bar', color='mediumpurple')
# plt.title('Top 10 Products by Quantity Sold')
# plt.xlabel('Product')
# plt.ylabel('Total Quantity')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('top_products.png')
# plt.show()
# print("Saved: top_products.png")

# print("\nEDA Complete. All charts saved.")

# ----------------------------------------------------------------------

# RFM Analysis

# # ── Load cleaned data ───────────────────────────────────
# df = pd.read_csv('online_retail_cleaned.csv')
# df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# # ── Step 1: Set reference date ──────────────────────────
# # We use the day after the last invoice as "today"
# reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
# print("Reference Date:", reference_date)

# # ── Step 2: Calculate RFM values ────────────────────────
# rfm = df.groupby('Customer ID').agg(
#     Recency   = ('InvoiceDate', lambda x: (reference_date - x.max()).days),
#     Frequency = ('Invoice', 'nunique'),
#     Monetary  = ('TotalPrice', 'sum')
# ).reset_index()

# print("\nRFM Table Sample:")
# print(rfm.head(10))
# print("\nRFM Shape:", rfm.shape)

# # ── Step 3: Score each metric 1-4 ──────────────────────
# # Recency: lower days = better = higher score (reverse)
# rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4,3,2,1])

# # Frequency: higher = better = higher score
# rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1,2,3,4])

# # Monetary: higher = better = higher score
# rfm['M_Score'] = pd.qcut(rfm['Monetary'], q=4, labels=[1,2,3,4])

# # ── Step 4: Create RFM Segment ──────────────────────────
# rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# # ── Step 5: Assign Segment Labels ──────────────────────
# def assign_segment(row):
#     r = int(row['R_Score'])
#     f = int(row['F_Score'])
#     m = int(row['M_Score'])
    
#     if r >= 3 and f >= 3 and m >= 3:
#         return 'Champions'
#     elif r >= 3 and f >= 2:
#         return 'Loyal Customers'
#     elif r >= 3 and f <= 2:
#         return 'Potential Loyalists'
#     elif r == 2 and f >= 2:
#         return 'At Risk'
#     elif r <= 2 and f <= 2 and m >= 3:
#         return 'Cannot Lose Them'
#     elif r == 1 and f >= 3:
#         return 'Hibernating'
#     else:
#         return 'Lost'

# rfm['Segment'] = rfm.apply(assign_segment, axis=1)

# # ── Step 6: Segment Summary ─────────────────────────────
# segment_summary = rfm.groupby('Segment').agg(
#     Customer_Count = ('Customer ID', 'count'),
#     Avg_Recency    = ('Recency', 'mean'),
#     Avg_Frequency  = ('Frequency', 'mean'),
#     Avg_Monetary   = ('Monetary', 'mean'),
#     Total_Revenue  = ('Monetary', 'sum')
# ).round(2).sort_values('Total_Revenue', ascending=False)

# print("\nSegment Summary:")
# print(segment_summary)

# # ── Step 7: Visualise Segments ──────────────────────────
# plt.figure(figsize=(10,5))
# rfm['Segment'].value_counts().plot(kind='bar', color='steelblue')
# plt.title('Customer Count by Segment')
# plt.xlabel('Segment')
# plt.ylabel('Number of Customers')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('rfm_segments.png')
# plt.show()
# print("Saved: rfm_segments.png")

# # ── Step 8: Save RFM table ──────────────────────────────
# rfm.to_csv('rfm_output.csv', index=False)
# print("\nRFM table saved as rfm_output.csv")

# ----------------------------------------------------------------------

# SQL Analysis

# ── Load both files ─────────────────────────────────────
# df = pd.read_csv('online_retail_cleaned.csv')
# rfm = pd.read_csv('rfm_output.csv')
# df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# # ── Create SQLite database in memory ───────────────────
# conn = sqlite3.connect('retail.db')
# df.to_sql('transactions', conn, if_exists='replace', index=False)
# rfm.to_sql('rfm', conn, if_exists='replace', index=False)
# print("Database created with tables: transactions, rfm")

# # ── Query 1: Total Revenue by Country ──────────────────
# q1 = pd.read_sql_query("""
#     SELECT Country,
#            ROUND(SUM(TotalPrice), 2) AS Total_Revenue,
#            COUNT(DISTINCT "Customer ID") AS Unique_Customers
#     FROM transactions
#     GROUP BY Country
#     ORDER BY Total_Revenue DESC
#     LIMIT 10
# """, conn)
# print("\nQuery 1 — Top 10 Countries by Revenue:")
# print(q1)

# # ── Query 2: Monthly Revenue ────────────────────────────
# q2 = pd.read_sql_query("""
#     SELECT STRFTIME('%Y-%m', InvoiceDate) AS Month,
#            ROUND(SUM(TotalPrice), 2) AS Monthly_Revenue,
#            COUNT(DISTINCT Invoice) AS Total_Orders
#     FROM transactions
#     GROUP BY Month
#     ORDER BY Month
# """, conn)
# print("\nQuery 2 — Monthly Revenue Trend:")
# print(q2)

# # ── Query 3: Customer Segment Summary ──────────────────
# q3 = pd.read_sql_query("""
#     SELECT Segment,
#            COUNT("Customer ID") AS Customer_Count,
#            ROUND(AVG(Monetary), 2) AS Avg_Monetary,
#            ROUND(SUM(Monetary), 2) AS Total_Revenue
#     FROM rfm
#     GROUP BY Segment
#     ORDER BY Total_Revenue DESC
# """, conn)
# print("\nQuery 3 — Revenue by Customer Segment:")
# print(q3)

# # ── Query 4: Top 10 Customers by Revenue ───────────────
# q4 = pd.read_sql_query("""
#     SELECT "Customer ID",
#            COUNT(DISTINCT Invoice) AS Total_Orders,
#            ROUND(SUM(TotalPrice), 2) AS Total_Revenue
#     FROM transactions
#     GROUP BY "Customer ID"
#     ORDER BY Total_Revenue DESC
#     LIMIT 10
# """, conn)
# print("\nQuery 4 — Top 10 Customers:")
# print(q4)

# # ── Query 5: Top 10 Best Selling Products ──────────────
# q5 = pd.read_sql_query("""
#     SELECT Description,
#            SUM(Quantity) AS Total_Quantity_Sold,
#            ROUND(SUM(TotalPrice), 2) AS Total_Revenue
#     FROM transactions
#     GROUP BY Description
#     ORDER BY Total_Quantity_Sold DESC
#     LIMIT 10
# """, conn)
# print("\nQuery 5 — Top 10 Best Selling Products:")
# print(q5)

# # ── Save all query results ──────────────────────────────
# q1.to_csv('sql_country_revenue.csv', index=False)
# q2.to_csv('sql_monthly_revenue.csv', index=False)
# q3.to_csv('sql_segment_summary.csv', index=False)
# q4.to_csv('sql_top_customers.csv', index=False)
# q5.to_csv('sql_top_products.csv', index=False)
# print("\nAll SQL query results saved as CSV files.")

# conn.close()