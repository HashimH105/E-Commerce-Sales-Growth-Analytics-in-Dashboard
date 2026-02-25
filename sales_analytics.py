import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import mysql.connector
from datetime import datetime
import numpy as np

# Step 1: Load original CSV data
print("Loading data from CSV...")
df = pd.read_csv('transactions_data.csv')

# Step 2: Clean data 
df.dropna(subset=['OrderID', 'CustomerID', 'OrderDate', 'ProductID', 'Category', 'Quantity', 'UnitPrice', 'Region'], inplace=True)
df.drop_duplicates(inplace=True)
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
df['Discount'] = df['Discount'].fillna(0)


# Revenue will be calculated automatically by MySQL generated column

# Step 3: Store to MySQL 
print("Connecting to MySQL and storing data...")
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root@h1hashim',                # ← change your credentials
    database='sales_growth_db'
)
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO transactions 
        (OrderID, CustomerID, OrderDate, ProductID, Category, Quantity, UnitPrice, Region, Discount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        CustomerID = VALUES(CustomerID),
        OrderDate = VALUES(OrderDate),
        ProductID = VALUES(ProductID),
        Category = VALUES(Category),
        Quantity = VALUES(Quantity),
        UnitPrice = VALUES(UnitPrice),
        Region = VALUES(Region),
        Discount = VALUES(Discount)
    """, (
        row['OrderID'], row['CustomerID'], row['OrderDate'].date(),
        row['ProductID'], row['Category'], row['Quantity'],
        row['UnitPrice'], row['Region'], row['Discount']
    ))

conn.commit()
conn.close()
print("Data successfully stored/updated in MySQL.")


# Step 4: Fetch cleaned data FROM MySQL (Revenue is now auto-calculated)
print("Fetching data from MySQL for analysis...")
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root@h1hashim',
    database='sales_growth_db'
)

df = pd.read_sql("SELECT * FROM transactions", conn)
conn.close()

# CRITICAL FIX: Convert OrderDate to datetime AFTER reading from MySQL
# (mysql-connector often returns DATE as object/string)
df['OrderDate'] = pd.to_datetime(df['OrderDate'])



# Step 5: Analyses

# 5.1 Monthly Sales Trends
df['Month'] = df['OrderDate'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_sales['Month'] = monthly_sales['Month'].dt.to_timestamp()

plt.figure(figsize=(10, 5))
sns.lineplot(x='Month', y='Revenue', data=monthly_sales)
plt.title('Monthly Sales Trends')
plt.savefig('trends.png')
plt.close()
print("Saved: trends.png")

# 5.2 Top Drivers (80/20 rule)


top_products  = df.groupby('ProductID')['Revenue'].sum().nlargest(5).reset_index()
top_regions   = df.groupby('Region')['Revenue'].sum().nlargest(3).reset_index()
top_customers = df.groupby('CustomerID')['Revenue'].sum().nlargest(10).reset_index()

# 5.3 RFM Segmentation

snapshot = df['OrderDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg({
    'OrderDate': lambda x: (snapshot - x.max()).days,
    'OrderID':   'count',
    'Revenue':   'sum'
}).rename(columns={'OrderDate': 'Recency', 'OrderID': 'Frequency', 'Revenue': 'Monetary'})

rfm['R'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F'] = pd.qcut(rfm['Frequency'], 4, labels=[1,2,3,4])
rfm['M'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])
rfm['RFM'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)
rfm = rfm.reset_index()

# 5.4 Cohort Analysis (Retention)

print("Calculating cohorts...")
df['CohortMonth'] = df.groupby('CustomerID')['OrderDate'].transform('min').dt.to_period('M')  

cohort_data = df.groupby(['CohortMonth', 'Month'])['CustomerID'].nunique().reset_index()
cohort_data['Period'] = (cohort_data['Month'] - cohort_data['CohortMonth']).apply(lambda x: x.n)

cohort_pivot = cohort_data.pivot_table(
    index='CohortMonth',
    columns='Period',
    values='CustomerID'
)
cohort_pivot = cohort_pivot.divide(cohort_pivot.iloc[:, 0], axis=0).reset_index()

print("Cohort pivot created.")

# 5.5 Simple Linear Forecast (next 6 months)

print("Generating forecast...")
monthly_sales['MonthNum'] = np.arange(len(monthly_sales))
X = monthly_sales['MonthNum'].values.reshape(-1, 1)
y = monthly_sales['Revenue']
model = LinearRegression().fit(X, y)

future_nums = np.arange(len(monthly_sales), len(monthly_sales) + 6).reshape(-1, 1)
forecast_revenue = model.predict(future_nums)


future_months = pd.date_range(
    start=monthly_sales['Month'].max() + pd.DateOffset(months=1),
    periods=6,
    freq='ME'
)

forecast = pd.DataFrame({'Month': future_months, 'Forecast_Revenue': forecast_revenue})

print("Exporting insights to CSV...")

category_sales = df.groupby('Category')['Revenue'].sum().reset_index()
region_sales = df.groupby('Region')['Revenue'].sum().reset_index()

insights_df = pd.concat([
    monthly_sales,
    top_products,
    top_regions,
    top_customers,
    rfm,
    cohort_pivot,
    forecast,
    category_sales,    
    region_sales       
], axis=1, ignore_index=False)
# Export full row-level data — BEST for Tableau visuals
df.to_csv('full_transactions_for_tableau.csv', index=False)
print("Exported full_transactions_for_tableau.csv — use THIS in Tableau!")