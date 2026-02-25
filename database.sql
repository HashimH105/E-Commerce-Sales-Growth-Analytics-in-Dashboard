REATE DATABASE IF NOT EXISTS sales_growth_db;

USE sales_growth_db;

CREATE TABLE IF NOT EXISTS transactions (
    OrderID INT PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    Region VARCHAR(50),
    Discount DECIMAL(5, 2),
    Revenue DECIMAL(12, 2) GENERATED ALWAYS AS (Quantity * UnitPrice * (1 - Discount)) STORED,
    ProductID VARCHAR(50),
    Category VARCHAR(100)
);

-- Add indexes for high-impact queries (speeds up trends, RFM, regional analysis)
ALTER TABLE transactions
ADD INDEX idx_orderdate (OrderDate),
ADD INDEX idx_customerid (CustomerID),
ADD INDEX idx_region (Region);