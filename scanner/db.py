import sqlite3
from paths import get_user_db_path

def get_connection():
    return sqlite3.connect(get_user_db_path())

def check_hash(sha256_hash):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute("SELECT malware_name, malware_family FROM malware_hashes WHERE sha256 = ?", (sha256_hash,))
        result = c.fetchone()
    except sqlite3.OperationalError as e:
        # handle missing-table gracefully (database may not have been initialized)
        if 'no such table' in str(e):
            print("Warning: database table 'malware_hashes' not found — run 'python scanner/init_db.py' or update hashes.")
            result = None
        else:
            raise
    finally:
        conn.close()

    return result


