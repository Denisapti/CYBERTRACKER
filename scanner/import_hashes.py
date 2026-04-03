import csv
import sqlite3
import os
import json
from datetime import datetime
from paths import get_user_csv_path, get_user_db_path, get_metadata_path

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

def import_user_hashes():
    """Import hashes from CSV into the database. Can be called multiple times."""
    CSV_PATH = get_user_csv_path()
    
    # Check if CSV exists
    if not os.path.exists(CSV_PATH):
        print(f"CSV file not found at {CSV_PATH}")
        return False
    
    conn = sqlite3.connect(get_user_db_path())
    cursor = conn.cursor()

    try:
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

        # --- write metadata so update/freshness checks can be reliable ---
        metadata_path = get_metadata_path()
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

        print("Import complete.")
        return True
    except Exception as e:
        print(f"Import failed: {e}")
        return False
    finally:
        conn.close()

# Legacy CLI support
if __name__ == "__main__":
    import_user_hashes()
