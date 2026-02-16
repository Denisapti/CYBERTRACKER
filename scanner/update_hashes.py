import os
import hashlib
import requests
import subprocess

#URL for downloading the latest MalwareBazaar CSV
CSV_URL = "https://bazaar.abuse.ch/export/csv/recent/"

#Path to the current CSV file used by the system
CSV_FILE = "scanner/data/hashes.csv"

#Temporary file used to compare new download before replacing
TMP_FILE = "scanner/data/hashes.csv.tmp"



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
#Purpose: Re_run import_hashes.py to rebuild database
#after CSV is updated
#---------------------------------------------------
def rebuild_database():
  print("Rebuilding database...")
  subprocess.run(["python", "scanner/import_hashes.py"], check=True)
#---------------------------------------------------
#Function: main
#Purpose: Controls update process
#1. Download latest CSV
#2. Compare with existing file
#3. Replace if changed
#4. Revuild database if needed
#---------------------------------------------------
def main():
  download_csv()

# If this is the first time (no CSV exists yet)
  if not os.path.exists(CSV_FILE):
    os.replace(TMP_FILE, CSV_FILE)
    print("Initial hashes.csv created.")
    rebuild_database()
    return

# Compare old and new fule hashes
old_hash = file_sha256(CSV_FILE)
new_hash = file_sha256(TMP_FILE)

if old_hash == new_hash:
  print("No update detected.")
  os.remove(TMP_FILE)
else:
  print("Update detected. Replacing hashes.csv...")
  os.replace(TMP_FILE, CSV_FILE)
  rebuild_database()
  print("Update complete.")

#Run the script
if  __name__=="__main__":
    main()

