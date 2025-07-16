import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    phone_number TEXT
)
""")
conn.commit()


def save_user(user_id: int, phone_number: str):
    cursor.execute("INSERT INTO users (user_id, phone_number) VALUES (?, ?)", (user_id, phone_number))
    conn.commit()


def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
