import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Create bills table
c.execute('''
CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

# Default users
c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("admin", "admin123"))
c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ("user1", "password1"))

conn.commit()
conn.close()
