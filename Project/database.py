import sqlite3
import bcrypt

def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('users.db', check_same_thread=False)
    return conn

def create_users_table():
    """Create the users table if it doesn't exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def register_user(username, password, email):
    """Register a new user with hashed password."""
    conn = create_connection()
    cursor = conn.cursor()
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute('''
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, email))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists

def verify_user(username, password):
    """Verify user credentials."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        hashed_password = row[0]
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True
    return False

def get_all_users():
    """Get all users (for admin purposes, optional)."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, created_at FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_users_table()
    print("Database and table created successfully.")