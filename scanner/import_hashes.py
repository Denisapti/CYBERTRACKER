import csv
import sqlite3
import os
import json
from datetime import datetime

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

# --- write metadata so update/freshness checks can be reliable ---
def _newest_first_seen_from_csv(path: str):
    newest = None
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader((line.lstrip('#').strip() for line in f if line.strip() and not line.startswith('##')),
                                skipinitialspace=True)
            for row in reader:
                if not row:
                    continue
                ts = row[0].strip().strip('"')
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    continue
                if newest is None or dt > newest:
                    newest = dt
    except Exception:
        return None
    return newest

metadata_path = os.path.join(BASE_DIR, "data", "metadata.json")
_newest = _newest_first_seen_from_csv(CSV_PATH)
if _newest:
    meta = {
        "last_api_timestamp": _newest.strftime("%Y-%m-%d %H:%M:%S"),
        "last_import_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open(metadata_path, "w", encoding="utf-8") as mf:
            json.dump(meta, mf)
        print(f"Metadata written to {metadata_path}")
    except Exception as e:
        print("Failed to write metadata:", e)
