#!/usr/bin/env python3
import sqlite3
from db import check_hash

# Get a known malware hash from the database
conn = sqlite3.connect("malware_hashes.db")
c = conn.cursor()
c.execute("SELECT sha256, malware_name, malware_family FROM malware_hashes LIMIT 1")
result = c.fetchone()
conn.close()

if result:
    known_hash, malware_name, malware_family = result
    print(f"Testing with known malware hash: {known_hash}")
    print(f"Expected: {malware_name} ({malware_family})\n")
    
    # Test the lookup
    result = check_hash(known_hash)
    if result:
        found_name, found_family = result
        print(f"✓ FOUND: {found_name} ({found_family})")
    else:
        print("✗ NOT FOUND (unexpected!)")
else:
    print("No hashes found in database!")
