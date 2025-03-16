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
    Country VARCHAR(255) NOT NULL,
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

execute_query(connection, create_customers_table)
execute_query(connection, create_orders_table)
execute_query(connection, create_products_table)
execute_query(connection, create_order_details_table)

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
    (1, 1, 1),  -- John 1 Laptop
    (1, 2, 1),  -- John 1 Coffee Maker
    (2, 2, 1),  -- Bob 1 Coffee Maker
    (3, 3, 1),  -- Alice 1 Smartphone
    (4, 4, 1);  -- Michael 1 Toaster
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
print(result_8)

connection.close()
