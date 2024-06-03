import sqlite3

DATABASE_URL = "test.db"

def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    return conn

# TODO: DELETE initialize
def initialize():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sports (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        slug TEXT,
                        active BOOLEAN)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        slug TEXT,
                        active BOOLEAN,
                        type TEXT,
                        sport_id INTEGER,
                        status TEXT,
                        scheduled_start TEXT,
                        actual_start TEXT,
                        FOREIGN KEY (sport_id) REFERENCES sports (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS selections (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        event_id INTEGER,
                        price REAL,
                        active BOOLEAN,
                        outcome TEXT,
                        FOREIGN KEY (event_id) REFERENCES events (id))''')
    conn.commit()
    conn.close()
