"""Database initialization wrapper for guaranteed schema setup."""
import os
from paths import get_user_db_path, get_user_csv_path
from init_db import init_user_db
from import_hashes import import_user_hashes

def ensure_user_db_exists():
    """
    Ensures the user database exists and is initialized.
    Idempotent - safe to call multiple times.
    
    Returns: path to the database
    """
    db_path = get_user_db_path()
    
    # Initialize schema if needed
    init_user_db()
    
    # If CSV exists but DB is empty, populate it
    csv_path = get_user_csv_path()
    if os.path.exists(csv_path):
        # Check if DB has any data
        import sqlite3
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM malware_hashes")
            count = cursor.fetchone()[0]
            conn.close()
            
            # Import only if DB is empty
            if count == 0:
                print("Database empty - importing hashes...")
                import_user_hashes()
        except Exception as e:
            print(f"Warning checking DB: {e}")
    
    return db_path
