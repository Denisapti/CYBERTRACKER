import os
import hashlib
import requests
import subprocess
from paths import get_user_csv_path, get_user_data_dir
from init_db import init_user_db
from import_hashes import import_user_hashes

#URL for downloading the latest MalwareBazaar CSV
CSV_URL = "https://bazaar.abuse.ch/export/csv/recent/"

#Path to the current CSV file used by the system
CSV_FILE = get_user_csv_path()

#Temporary file used to compare new download before replacing
TMP_FILE = os.path.join(get_user_data_dir(), "hashes.csv.tmp")



#-----------------------------------------------------
#Function: file_sha256
#Purpose: Generate SHA-256 hash of a file
#Used to compare old vs new CSV to detect changes
#----------------------------------------------------
def file_sha256(path):
  sha256 = hashlib.sha256()
  with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(8192), b""):
      sha256.update(chunk)
  return sha256.hexdigest()
#----------------------------------------------------
#Function: download_csv
#Purpose: Download the latest CSV from MalwareBazaar
#Saves it as a temporary file
#---------------------------------------------------
def download_csv():
  print("Downloading latest CSV from MalwareBazaar...")
  response = requests.get(CSV_URL, timeout=60)
  response.raise_for_status()

  with open(TMP_FILE, "wb") as f:
    f.write(response.content)
#---------------------------------------------------
#Function: rebuild_database
#Purpose: Initialize DB schema and import hashes
#after CSV is updated
#---------------------------------------------------
def rebuild_database():
  print("Rebuilding database...")
  # ensure DB schema exists before importing rows
  init_user_db()
  import_user_hashes()
#---------------------------------------------------
#Function: main
#Purpose: Controls update process
#1. Download latest CSV
#2. Compare with existing file
#3. Replace if changed
#4. Revuild database if needed
#---------------------------------------------------
def main(force: bool = False):
  download_csv()

  # ensure DB schema exists (idempotent)
  init_user_db()

  # If this is the first time (no CSV exists yet)
  if not os.path.exists(CSV_FILE):
    os.replace(TMP_FILE, CSV_FILE)
    print("Initial hashes.csv created.")
    rebuild_database()
    return

  # Compare old and new file hashes
  old_hash = file_sha256(CSV_FILE)
  new_hash = file_sha256(TMP_FILE)

  if old_hash == new_hash:
    print("No update detected.")
    # honor explicit force request
    if force:
      print("Force flag set — rebuilding database despite identical CSV...")
      os.remove(TMP_FILE)
      rebuild_database()
      print("Force rebuild complete.")
      return
    else:
      print("No import required. To force a rebuild use --force.")
      os.remove(TMP_FILE)
      return
  else:
    print("Update detected. Replacing hashes.csv...")
    os.replace(TMP_FILE, CSV_FILE)
    rebuild_database()
    print("Update complete.")

#Run the script
if __name__ == "__main__":
    import sys
    force_flag = "--force" in sys.argv or "--force-update" in sys.argv
    main(force=force_flag)

