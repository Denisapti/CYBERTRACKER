import sys
import json
from hashing import sha256_file
from db import check_hash

def main(file_path):
    file_hash = sha256_file(file_path)
    result = check_hash(file_hash)

    if result:
        malware_name, malware_family = result
        verdict = {
            "file_hash": file_hash,
            "known_malware": True,
            "malware_name": malware_name,
            "malware_family": malware_family,
            "detection_method": "Threat intelligence hash match"
        }
    else:
        verdict = {
            "file_hash": file_hash,
            "known_malware": False,
            "detection_method": "No match in threat intelligence database"
        }

    print(json.dumps(verdict, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    main(sys.argv[1])
