import sqlite3
import os
import database # Import the database module itself

def initialize_database():
    """Initializes the SQLite database and table, logging the result."""
    print("--- Database Initialization Start ---")
    
    # Check folder path first, using the path defined in the imported database module
    db_dir = os.path.dirname(database.DB_PATH)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            print(f"Directory created successfully: {db_dir}")
        except Exception as e:
            print(f"ERROR: Could not create directory {db_dir}. Check file permissions! Error: {e}")
            return
            
    # Use functions from the imported database module
    conn = database.create_connection()
    if conn:
        try:
            database.create_users_table(conn)
            print(f"SUCCESS: Database and 'users' table initialized at {database.DB_PATH}")
        except Exception as e:
            print(f"ERROR: Failed to create 'users' table. Error: {e}")
        finally:
            conn.close()
    else:
        print("ERROR: Failed to establish database connection.")
        
    print("--- Database Initialization End ---")

if __name__ == "__main__":
    # If this script is run directly, initialize the database
    initialize_database()

# This part ensures initialization runs when imported (like in app.py)
initialize_database()
