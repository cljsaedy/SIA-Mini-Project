import sqlite3
import hashlib

def create_database():
    # Connect to the database (this creates the file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create a table to store users
    # We store the username and the hashed password (not the plain text!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # Let's add a default user so you can log in immediately
    # Username: admin
    # Password: password123
    
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

    # Save changes and close
    conn.commit()
    conn.close()
    print("Database setup complete. 'users.db' has been created.")

if __name__ == "__main__":
    create_database()