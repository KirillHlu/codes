import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite: Success")
    except Error as e:
        print(f"Error: {e}")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"Error: {e}")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error: {e}")

connection = create_connection("data_base.sqlite")
cursor = connection.cursor()

create_customers_table = """
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    City VARCHAR(255) NOT NULL,
    Country VARCHAR(255) NOT NULL
);
"""

create_orders_table = """
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    OrderDate DATE NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL
);
"""

create_products_table = """
CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName VARCHAR(255) NOT NULL,
    Category VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);
"""

create_order_details_table = """
CREATE TABLE IF NOT EXISTS OrderDetails (
    OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER NOT NULL
);
"""

# execute_query(connection, create_customers_table)
# execute_query(connection, create_orders_table)
# execute_query(connection, create_products_table)
# execute_query(connection, create_order_details_table)

create_customers = """
INSERT INTO Customers (FirstName, LastName, City, Country)
VALUES
    ("John", "Smith", "New York", "USA"),
    ("Bob", "Werth", "Wellington", "New Zealand"),
    ("Alice", "Johnson", "Toronto", "Canada"),
    ("Michael", "Brown", "Boston", "USA");
"""

create_products = """
INSERT INTO Products (ProductName, Category, Price)
VALUES
    ("Laptop", "Electronics", 999.99),
    ("Coffee Maker", "Appliances", 49.99),
    ("Smartphone", "Electronics", 699.99),
    ("Toaster", "Appliances", 29.99);
"""

create_orders = """
INSERT INTO Orders (CustomerID, OrderDate, TotalAmount)
VALUES
    (1, "2023-10-01", 1049.98),
    (2, "2023-10-02", 49.99),
    (3, "2023-10-03", 699.99),
    (4, "2023-10-04", 29.99),
    (1, "2023-10-01", 49.99);
"""

create_order_details = """
INSERT INTO OrderDetails (OrderID, ProductID, Quantity)
VALUES
    (1, 1, 1),
    (1, 2, 1),
    (2, 2, 1),
    (3, 3, 1),
    (4, 4, 1);
"""

# execute_query(connection, create_customers)
# execute_query(connection, create_products)
# execute_query(connection, create_orders)
# execute_query(connection, create_order_details)

print("\n5th query:")
query_1 = """
SELECT FirstName, LastName
from Customers where Customers.Country = ?
"""
cursor.execute(query_1, ('USA',))
result_1 = cursor.fetchall()
i = 1
for first_name, last_name in result_1:
    print(f"  {i}) {first_name} {last_name}")
    i += 1

print("\n6th query:")
query_2 = """
SELECT AVG(Price) from Products
"""
cursor.execute(query_2)
result_2 = cursor.fetchall()
print(f"  Average price: {result_2[0][0]} $")


print("\n7th query:")
query_4 = """
SELECT CustomerID, COUNT(*) AS OrderCount
FROM Orders
GROUP BY CustomerID;
"""

cursor.execute(query_4)
result_4 = cursor.fetchall()

for customer_id, order_count in result_4:
    print(f"  {customer_id}: {order_count}")

print("\n8th query:")
query_5 = """
SELECT CustomerID, SUM(TotalAmount) AS OrdersPrice
FROM Orders
GROUP BY CustomerID;
"""
cursor.execute(query_5)
result_5 = cursor.fetchall()
for customer_id, order_sum in result_5:
    print(f"  {customer_id}: {order_sum} $")

print("\n9th query:")
query_6 = """
SELECT Customers.FirstName, Customers.LastName, Orders.OrderID, Orders.OrderDate from Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
"""
cursor.execute(query_6)
result_6 = cursor.fetchall()
for first_name, last_name, order_id, order_date in result_6:
    print(f"  {first_name} {last_name} {order_id} {order_date}")

print("\n10th query:")
query_7 = """
SELECT Products.ProductName, SUM(OrderDetails.Quantity) FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
GROUP BY Products.ProductName
"""

cursor.execute(query_7)
result_7 = cursor.fetchall()
for product_name, product_count in result_7:
    print(f"  {product_name}: {product_count}")

print("\n11th query")
query_8 = """
SELECT Customers.FirstName, Customers.LastName, Products.ProductName, OrderDetails.Quantity
FROM OrderDetails
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
JOIN Products ON OrderDetails.ProductID = Products.ProductID;
"""
cursor.execute(query_8)
result_8 = cursor.fetchall()
for first_name, last_name, product_name, quantity in result_8:
    print(f"  {first_name} {last_name} ordered {quantity} unit(s) of {product_name}")

print("\n12th query:")
query_9 = """
SELECT Customers.FirstName, Customers.LastName
FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CustomerID
HAVING SUM(Orders.TotalAmount) > (SELECT AVG(TotalAmount) FROM Orders);
"""
cursor.execute(query_9)
result_9 = cursor.fetchall()
for first_name, last_name in result_9:
    print(f"  {first_name} {last_name}")

print("\n13th query:")
query_10 = """
SELECT ProductName
FROM Products
WHERE ProductID = (
    SELECT ProductID
    FROM OrderDetails
    GROUP BY ProductID
    ORDER BY SUM(Quantity) DESC
);
"""
cursor.execute(query_10)
result_10 = cursor.fetchall()
for product_name in result_10:
    print(f"  The most ordered product: {product_name[0]}")

print("\n14th query:")
query_14 = """
SELECT Customers.FirstName, Customers.LastName
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
WHERE Orders.OrderID IS NULL
  AND Orders.CustomerID IS NOT NULL;
"""
cursor.execute(query_14)
result_14 = cursor.fetchall()

if result_14:
    for first_name, last_name in result_14:
        print(f"  {first_name} {last_name}")
else:
    print("  No customers without orders found.")

print("\n15th query:")
query_15 = """
SELECT Customers.FirstName, Customers.LastName, SUM(Orders.TotalAmount) AS TotalAmount
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CustomerID;
"""
cursor.execute(query_15)
result_15 = cursor.fetchall()

for first_name, last_name, total_amount in result_15:
    print(f"  {first_name} {last_name}: {total_amount} $")

query_1 = """
SELECT Customers.FirstName, Customers.LastName
FROM Customers
WHERE (
    SELECT COUNT(DISTINCT strftime('%Y-%m', Orders.OrderDate))
    FROM Orders
    WHERE Orders.CustomerID = Customers.CustomerID
) = 1;
"""

cursor.execute(query_1)
result_1 = cursor.fetchall()
print("\nOften buyers:")
for first_name, last_name in result_1:
    print(f"  {first_name} {last_name}")

query_2 = """
SELECT Products.Category, strftime('%Y-%m', Orders.OrderDate) AS YearMonth, SUM(OrderDetails.Quantity * Products.Price) AS TotalSales
FROM OrderDetails
JOIN Products ON OrderDetails.ProductID = Products.ProductID
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
WHERE Orders.OrderDate >= date('now', '-1 year')
GROUP BY Products.Category, YearMonth
ORDER BY Products.Category, YearMonth;
"""

cursor.execute(query_2)
result_2 = cursor.fetchall()
print("\nMost profitable categories:")

for el in result_2:
    print(el)

query_3 = """
WITH ExpensiveProducts AS (SELECT ProductID FROM Products WHERE Price > (SELECT AVG(Price) FROM Products)),
QualifiedOrders AS (SELECT Orders.CustomerID, Orders.OrderIDFROM Orders
JOIN OrderDetails ON OrderDetails.OrderID = OrderDetails.OrderID
WHERE OrderDetails.ProductID IN (SELECT ProductID FROM ExpensiveProducts))
SELECT Customers.FirstName, Customers.LastName
FROM Customers
JOIN QualifiedOrders ON Customers.CustomerID = QualifiedOrders.CustomerID
GROUP BY Customers.CustomerID
HAVING COUNT(DISTINCT QualifiedOrders.OrderID) >= 2;
"""
cursor.execute(query_2)
result_3 = cursor.fetchall()
print(result_3)

query_4 = """
SELECT DISTINCT Products.ProductName
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
WHERE Products.ProductID NOT IN (
SELECT DISTINCT Products.ProductID
FROM Products
JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
JOIN Customers ON Orders.CustomerID = Customers.CustomerID
WHERE Customers.Country != 'USA');
"""

cursor.execute(query_4)
result_4 = cursor.fetchall()
print("\nProducts for one country:")
for el in result_4:
    print(f"  {el[0]}")

query_5 = """
WITH CountryAvg AS (
SELECT Customers.Country,
CASE WHEN COUNT(Orders.OrderID) = 0 THEN 0 
ELSE AVG(Orders.TotalAmount) END AS AvgAmount
FROM Customers
LEFT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.Country)
SELECT CountryAvg1.Country AS Country1, CountryAvg2.Country AS Country2, ABS(CountryAvg1.AvgAmount - CountryAvg2.AvgAmount) AS AvgDifference
FROM CountryAvg AS CountryAvg1
CROSS JOIN CountryAvg AS CountryAvg2
WHERE CountryAvg1.Country < CountryAvg2.Country
ORDER BY CountryAvg1.Country, CountryAvg2.Country;
"""

cursor.execute(query_5)
result_5 = cursor.fetchall()
print("\nCountry's compare:")
for couple in result_5:
    print(f"  {couple[0]} and {couple[1]}: {couple[2]} $")

query_3 = """
SELECT 
    Category,
    COUNT(ProductID) AS ProductCount
FROM 
    Products
GROUP BY 
    Category;
"""

cursor.execute(query_3)
result_3 = cursor.fetchall()
print("\n3rd task:")
for el in result_3:
    print(f"  {el[0]}: {el[1]}")

print("\nTask 4th")
task_4 = '''
SELECT Customers.FirstName, Customers.LastName FROM Customers
JOIN Orders ON Customers.CustomerID = Orders.CustomerID
GROUP BY Customers.CustomerID
HAVING SUM(Orders.TotalAmount) > (SELECT AVG(TotalAmount) FROM Orders);
'''
results_4 = cursor.execute(task_4).fetchall()
for el in results_4:
    print(f"  {el[0]} {el[1]}")

print("\nTask 5th")
task_5 = '''
WITH ProductPurchases AS (
    SELECT Products.ProductID, Products.ProductName, Products.Category, Customers.CustomerID, Customers.FirstName, Customers.LastName,SUM(OrderDetails.Quantity) AS TotalQuantity
    FROM Products
    JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
    JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
    JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    GROUP BY  Products.ProductID, Customers.CustomerID
),
MaxPurchases AS (
    SELECT ProductID, MAX(TotalQuantity) AS MaxQuantity 
    FROM ProductPurchases 
    GROUP BY ProductID
) 
SELECT ProductPurchases.ProductName, ProductPurchases.Category, ProductPurchases.FirstName, ProductPurchases.LastName,ProductPurchases.TotalQuantity FROM ProductPurchases
JOIN MaxPurchases ON ProductPurchases.ProductID = MaxPurchases.ProductID AND ProductPurchases.TotalQuantity = MaxPurchases.MaxQuantity
ORDER BY ProductPurchases.ProductName;
'''

cursor.execute(task_5)
result_5 = cursor.fetchall()

for product, category, first, last, q in result_5:
    print(f"  {product} ({category}): {first} {last} bought {q}")
