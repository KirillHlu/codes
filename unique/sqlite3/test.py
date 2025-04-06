import sqlite3

conn = sqlite3.connect('car_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS body (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS engine (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS brand (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    id_body_standard INTEGER,
    FOREIGN KEY (id_body_standard) REFERENCES body(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS car (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    power REAL,
    id_brand INTEGER NOT NULL,
    id_body INTEGER NOT NULL,
    id_engine INTEGER NOT NULL,
    FOREIGN KEY (id_brand) REFERENCES brand(id),
    FOREIGN KEY (id_body) REFERENCES body(id),
    FOREIGN KEY (id_engine) REFERENCES engine(id)
)
''')

# cursor.execute("INSERT INTO body (id, name) VALUES (1, 'Sedan')")
# cursor.execute("INSERT INTO body (id, name) VALUES (2, 'SUV')")
# cursor.execute("INSERT INTO body (id, name) VALUES (3, 'Hatchback')")
#
# cursor.execute("INSERT INTO engine (id, name) VALUES (1, '1.6L Turbo')")
# cursor.execute("INSERT INTO engine (id, name) VALUES (2, '2.0L Diesel')")
# cursor.execute("INSERT INTO engine (id, name) VALUES (3, 'Electric')")
#
# cursor.execute("INSERT INTO brand (id, name, id_body_standard) VALUES (1, 'Toyota', 2)")
# cursor.execute("INSERT INTO brand (id, name, id_body_standard) VALUES (2, 'BMW', 1)")
# cursor.execute("INSERT INTO brand (id, name, id_body_standard) VALUES (3, 'Tesla', 1)")
#
# cursor.execute("INSERT INTO car (id, name, power, id_brand, id_body, id_engine) VALUES (1, 'Camry', 280, 1, 1, 1)")
# cursor.execute("INSERT INTO car (id, name, power, id_brand, id_body, id_engine) VALUES (2, 'X5', 300, 2, 2, 2)")
# cursor.execute("INSERT INTO car (id, name, power, id_brand, id_body, id_engine) VALUES (3, 'Model 3', 200, 3, 1, 3)")
#
# conn.commit()


query_1 = """
SELECT DISTINCT
    car.name, brand.name, engine.name, car.power 
FROM car
JOIN brand ON car.id_brand = brand.id
JOIN engine ON car.id_engine = engine.id
WHERE car.power > (SELECT AVG(power) FROM car)
ORDER BY car.power ASC
"""

cursor.execute(query_1)
result_1 = cursor.fetchall()
print("More than average power:")
for name, brand, engine, power in result_1:
    print(f"  {name}: {brand}, {engine}, {power}")

query_2 = """
SELECT car.name, brand.name, engine.name, body.name, car.power
FROM car
JOIN brand ON car.id_brand = brand.id
JOIN engine ON car.id_engine = engine.id
JOIN body ON car.id_body = body.id
WHERE car.power = (SELECT MAX(power) FROM car)
"""

cursor.execute(query_2)
result_2 = cursor.fetchall()
print("\nCar with max power:")
print(f"{result_2[0][0]}: {result_2[0][1]}, {result_2[0][2]}, {result_2[0][3]}, {result_2[0][4]}")

conn.close()
