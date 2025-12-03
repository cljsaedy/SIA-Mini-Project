import sqlite3
import hashlib

DB_NAME = 'users.db'

def initialize_db():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def check_credentials(username, password):
    """Returns True if login is correct, False otherwise."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    
    if result and result[0] == hashed_password:
        return True
    return False

def add_new_user(username, password):
    """Tries to add a new user. Returns True if success, False if username exists."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()