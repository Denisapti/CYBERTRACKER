import sqlite3

DB_PATH = "malware_hashes.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def check_hash(sha256_hash):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT malware_name, malware_family FROM malware_hashes WHERE sha256 = ?", (sha256_hash,))
    result = c.fetchone()

    conn.close()
    return result


