import sqlite3
from paths import get_user_db_path

def init_user_db():
    """Initialize the malware hashes database schema. Idempotent - safe to call multiple times."""
    conn = sqlite3.connect(get_user_db_path())
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS malware_hashes (
        sha256 TEXT PRIMARY KEY,
        malware_name TEXT,
        malware_family TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized.")

if __name__ == "__main__":
    conn = sqlite3.connect(get_user_db_path())
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS malware_hashes (
        sha256 TEXT PRIMARY KEY,
        malware_name TEXT,
        malware_family TEXT,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized.")
    #Run once via terminal: python init_db.py