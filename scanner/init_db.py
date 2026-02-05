import sqlite3

conn = sqlite3.connect("malware_hashes.db")
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