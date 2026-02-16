import os
import hashlib
import requests
import subprocess

CSV_URL = "https://bazaar.abuse.ch/export/csv/recent/"
CSV_FILE = "scanner/data/hashes.csv"
TMP_FILE = "scanner/data/hashes.csv.tmp"

def file_sha256(path):
  sha256 = hashlib.sha256()
  with open(path, "rb") as f:
    for chunk in iter(lambda: f.read(8192), b""):
      sha256.update(chunk)
      return sha256.hexdigest()

def download_csv():
  print("Downloading latest CSV from MalwareBazaar...")
  response = requests.get(CSV_URL, timeout=60)
  response.raise_for_status()

  with open(TMP_FILE, "wb") as f:
    f.write(response.content)

def rebuild_database():
  print("Rebuilding database...")
  subprocess.run(["python", "scanner/import_hashes.py"], check=True)

def main():
  downlaod_csv()

if not os.path.exists(CSV_FILE):
  os.replace(TMP_FILE, CSV_FILE)
  print("Initial hashes.csv created.")
  rebuild_database()
  return

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

if  __name__=="__main__":
    main()

