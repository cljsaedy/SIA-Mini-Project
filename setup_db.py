import sqlite3
import hashlib

def create_database():
    # Connect to the database (this creates the file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create a table to store users
    # Store the username and the hashed password 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # Default User
    
    default_user = "admin"
    default_pass = "password123"
    
    # Hash the default password before storing it
    # We use SHA-256 for security
    hashed_pass = hashlib.sha256(default_pass.encode()).hexdigest()
    
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                       (default_user, hashed_pass))
        print(f"Success! User '{default_user}' added to database.")
    except sqlite3.IntegrityError:
        print("User 'admin' already exists in the database.")

    conn.commit()
    conn.close()
    print("Database setup complete. 'users.db' has been created.")

if __name__ == "__main__":
    create_database()