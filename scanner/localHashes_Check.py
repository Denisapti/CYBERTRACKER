import os
import csv
from datetime import datetime
from paths import get_user_csv_path

file_path = get_user_csv_path()

# Try to determine the newest `first_seen_utc` value inside the CSV itself
# (this matches the timestamp returned by the MalwareBazaar API). If parsing
# fails, fall back to the file modification time.

def _newest_first_seen_from_csv(path: str):
    newest = None
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader((line.lstrip('#').strip() for line in f if line.strip() and not line.startswith('##')),
                                skipinitialspace=True)
            for row in reader:
                # header line will contain 'first_seen' as the first field; skip it
                if not row:
                    continue
                # Normalize quoted values and take first column as timestamp
                ts = row[0].strip().strip('"')
                try:
                    dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                except Exception:
                    # header or malformed line — skip
                    continue
                if newest is None or dt > newest:
                    newest = dt
    except FileNotFoundError:
        return None
    return newest


_newest = _newest_first_seen_from_csv(file_path)
if _newest:
    last_modified = _newest.strftime("%Y-%m-%d %H:%M:%S")
else:
    # fallback to filesystem modification time
    try:
        if os.path.exists(file_path):
            mod_timestamp = os.path.getmtime(file_path)
            last_modified = datetime.fromtimestamp(mod_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        else:
            # CSV doesn't exist yet; use placeholder
            last_modified = None
    except Exception:
        last_modified = None

if last_modified:
    print("The local hashes file was last modified on:", last_modified)
else:
    print("Local hashes file not yet initialized.")