import sqlite3
import os
import hashlib

# Define the path to your database file
DB_PATH = os.path.join("database", "users.db")

def create_connection():
    """Create and return a database connection."""
    conn = None
    try:
        
        db_dir = os.path.dirname(DB_PATH)
        if not os.path.exists(db_dir) and db_dir:
        
            os.makedirs(db_dir, exist_ok=True)
            
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_users_table(conn): 
    """Create the users table if it does not exist."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                vehicles TEXT
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating users table: {e}")

def add_user(conn, email, name, password_hash, vehicles=""):
    """Insert a new user into the database."""
    try:
        cursor = conn.cursor()
      
        cursor.execute(
            "INSERT INTO users (email, name, password_hash, vehicles) VALUES (?, ?, ?, ?)",
            (email, name, password_hash, vehicles)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        
        return False
    except sqlite3.Error as e:
        print(f"Error adding user: {e}")
        return False

def get_user(conn, email):
    """Fetch user details by email."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email, name, password_hash, vehicles FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            
            return {
                "email": row[0],
                "name": row[1],
                "password_hash": row[2],
                # vehicles column contains a comma-separated string, convert back to a list
                "vehicles": row[3].split(',') if row[3] else []
            }
        return None
    except sqlite3.Error as e:       
        print(f"Error fetching user: {e}")
        return None

# NOTE: The automatic database initialization block has been removed from here
# to prevent the circular import error.
