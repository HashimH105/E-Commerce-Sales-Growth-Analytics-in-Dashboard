import pandas as pd
import numpy as np
from datetime import datetime

np.random.seed(42)
dates = pd.date_range('2023-01-01', '2024-12-31')
data = {
    'OrderID': np.arange(1, 1001),
    'CustomerID': np.random.randint(1, 200, 1000),
    'OrderDate': np.random.choice(dates, 1000),
    'ProductID': [f'P{i}' for i in np.random.randint(1, 50, 1000)],
    'Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 1000),
    'Quantity': np.random.randint(1, 10, 1000),
    'UnitPrice': np.random.uniform(10, 500, 1000).round(2),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 1000),
    'Discount': np.random.uniform(0, 0.3, 1000).round(2)
    # Revenue will be auto-calculated in MySQL or Python
}
pd.DataFrame(data).to_csv('transactions_data.csv', index=False)
print("Sample data generated: transactions_data.csv")