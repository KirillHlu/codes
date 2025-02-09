import sqlite3
from sqlite3 import Error
from collections import Counter

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
    (2400, '2023-10-03 14:00:00', 3, '2023-10-03 14:40:00', 1, '03', 'Зарегистрированный', '67890', 1990, 'Ж'),
    (2400, '2023-10-03 14:00:00', 3, '2023-10-03 14:40:00', 1, 'B003', 'Зарегистрированный', '67890', 1990, 'Ж'),
    (3600, '2023-10-03 14:00:00', 3, '2023-10-03 14:40:00', 3, 'B002', 'Зарегистрированный', '67890', 2000, 'М')
"""


# execute_query(connection, create_trips_table)
# execute_query(connection, create_trips)

select_trips = "SELECT * FROM trips;"
trips = execute_read_query(connection, select_trips)

for trip in trips:
    print(trip)

cursor = connection.cursor()
cursor.execute("SELECT MAX(duration) FROM trips;")
max_duration = cursor.fetchone()[0]
print(f"Max duration: {max_duration}")

cursor = connection.cursor()
cursor.execute("SELECT COUNT(duration) FROM trips WHERE sub_type = 'Зарегистрированный'")
max_duration = cursor.fetchone()[0]
print(f"Count: {max_duration}")

cursor = connection.cursor()
cursor.execute("SELECT AVG(duration) FROM trips")
avg_duration = cursor.fetchone()[0]
print(f"Average duration: {avg_duration}")

cursor = connection.cursor()
cursor.execute("SELECT AVG(duration) FROM trips WHERE sub_type = 'Зарегистрированный'")
avg_duration_registered = cursor.fetchone()[0]

cursor = connection.cursor()
cursor.execute("SELECT AVG(duration) FROM trips where sub_type = 'Случайный'")
avg_duration_somebody = cursor.fetchone()[0]

if avg_duration_somebody > avg_duration_registered:      print(f"By unknowns ({avg_duration_somebody})")
elif avg_duration_somebody < avg_duration_registered:    print(f"By registered ({avg_duration_registered})")
else:                                             print(f"They're similar ({avg_duration_registered})")

select_trips = """
SELECT bike_number
FROM trips
"""
trips = execute_read_query(connection, select_trips)
list1 = []

for trip in trips:
    list1.append(trip[0])

counter = Counter(list1)

most_common_element, count = counter.most_common(1)[0]

print(f"Most common bike: {most_common_element}")

cursor = connection.cursor()
cursor.execute("SELECT AVG(duration) FROM trips WHERE CAST(strftime('%Y', start_date) AS INTEGER) - birth_date >= 30")
avg_duration_30_age = cursor.fetchone()[0]
print(f"Average duration by adults: {avg_duration_30_age}")

connection.close()
