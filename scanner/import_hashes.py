import csv
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "data", "hashes.csv")

conn = sqlite3.connect("malware_hashes.db")
cursor = conn.cursor()

with open(CSV_PATH, newline='', encoding="utf-8") as csvfile:
    # Process lines: skip pure comment lines, but keep and clean the header
    processed_lines = []
    for line in csvfile:
        if line.startswith("#") and ',' in line and '"' in line:
            # This is the header line (starts with # but contains quoted field names)
            processed_lines.append(line.lstrip("#").lstrip())
        elif not line.startswith("#"):
            # Keep data lines, skip pure comment lines
            processed_lines.append(line)
    
    reader = csv.DictReader(processed_lines, skipinitialspace=True)

    for row in reader:
        try:
            cursor.execute("""
            INSERT OR IGNORE INTO malware_hashes (sha256, malware_name, malware_family, source)
            VALUES (?, ?, ?, ?)
            """, (
                row["sha256_hash"].strip().lower(),
                row.get("signature", "Unknown"),
                row.get("file_type_guess", "Unknown"),
                row.get("reporter", "MalwareBazaar")
            ))
        except Exception as e:
            print("Error inserting row:", e)

conn.commit()
conn.close()

print("Import complete.")
