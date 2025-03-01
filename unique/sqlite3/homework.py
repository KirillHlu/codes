import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    use_id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id_order INTEGER PRIMARY KEY,
    use_id INTEGER,
    goods_id INTEGER,
    FOREIGN KEY (use_id) REFERENCES users (use_id),
    FOREIGN KEY (goods_id) REFERENCES goods (goods_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS goods (
    goods_id INTEGER PRIMARY KEY,
    name TEXT,
    price INTEGER
)
''')

# cursor.execute("INSERT INTO users (use_id, name, age) VALUES (1, 'John', 20)")
# cursor.execute("INSERT INTO users (use_id, name, age) VALUES (2, 'Bob', 25)")
# cursor.execute("INSERT INTO users (use_id, name, age) VALUES (3, 'Mary', 30)")
#
# cursor.execute("INSERT INTO goods (goods_id, name, price) VALUES (201, 'Laptop', 1500)")
# cursor.execute("INSERT INTO goods (goods_id, name, price) VALUES (202, 'Phone', 1000)")
# cursor.execute("INSERT INTO goods (goods_id, name, price) VALUES (203, 'Tablet', 1200)")
#
# cursor.execute("INSERT INTO orders (id_order, use_id, goods_id) VALUES (101, 1, 201)")
# cursor.execute("INSERT INTO orders (id_order, use_id, goods_id) VALUES (106, 1, 203)")
# cursor.execute("INSERT INTO orders (id_order, use_id, goods_id) VALUES (102, 2, 202)")
# cursor.execute("INSERT INTO orders (id_order, use_id, goods_id) VALUES (103, 1, 203)")
#
# conn.commit()

query_1 = '''
SELECT users.name, goods.name
from orders
JOIN users ON orders.use_id = users.use_id
JOIN goods ON orders.goods_id = goods.goods_id
'''
cursor.execute(query_1)
result_1 = cursor.fetchall()
print("Orders:")
for row in result_1:
    print(row)

user_name = 'John'
query_2 = '''
SELECT goods.name, goods.name
from orders
JOIN users on orders.use_id = users.use_id
JOIN goods on orders.goods_id = goods.goods_id
WHERE users.name = ?
'''
cursor.execute(query_2, (user_name,))
result_2 = cursor.fetchall()
print(f"\n{user_name}'s goods:")
for row in result_2:
    print(row[0])

query_3 = '''
SELECT users.name, SUM(goods.price) as total_spent
FROM orders
JOIN goods ON orders.goods_id = goods.goods_id
JOIN users ON orders.use_id = users.use_id
GROUP BY users.name
ORDER BY total_spent DESC
LIMIT 1
'''
cursor.execute(query_3)
result_3 = cursor.fetchone()
print(f"\nMax: {result_3[0]} ({result_3[1]}$)")

conn.close()
