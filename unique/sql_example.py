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

create_trips_table = """
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    duration INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    start_station INTEGER NOT NULL,
    end_date TEXT NOT NULL,
    end_station INTEGER NOT NULL,
    bike_number TEXT NOT NULL,
    sub_type TEXT CHECK(sub_type IN ('Зарегистрированный', 'Случайный')) NOT NULL,
    zip_code TEXT,
    birth_date INTEGER,
    gender TEXT CHECK(gender IN ('М', 'Ж'))
);
"""

create_trips = """
INSERT INTO trips (duration, start_date, start_station, end_date, end_station, bike_number, sub_type, zip_code, birth_date, gender)
VALUES
    (3600, '2023-10-01 10:00:00', 1, '2030-10-01 11:00:00', 2, 'B001', 'Зарегистрированный', '12345', 1985, 'М'),
    (7200, '2023-10-02 09:00:00', 2, '2023-10-02 09:30:00', 3, 'B002', 'Случайный', NULL, NULL, NULL),
    (2400, '2023-10-03 14:00:00', 3, '2023-10-03 14:40:00', 1, '03', 'Зарегистрированный', '67890', 1990, 'Ж');
"""


execute_query(connection, create_trips_table)
execute_query(connection, create_trips)

select_trips = "SELECT * FROM trips;"
trips = execute_read_query(connection, select_trips)

for trip in trips:
    print(trip)

cursor = connection.cursor()
cursor.execute("SELECT MAX(duration) FROM trips;")
max_duration = cursor.fetchone()[0]
print(f"Max duration: {max_duration}")

cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM trips WHERE sub_type = 'Зарегистрированный'")
max_duration = cursor.fetchone()[0]
print(f"Count: {max_duration}")

cursor = connection.cursor()
cursor.execute("SELECT AVG(duration) FROM trips")
avg_duration = cursor.fetchone()[0]
print(f"Average duration: {avg_duration}")

connection.close()
