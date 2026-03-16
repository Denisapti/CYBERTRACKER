import sys
import json
from hashing import sha256_file
from db import check_hash
from API_LocalComparison import main as check_db
from file_type_detector import investigate_file
from update_hashes import main as update_hashes_main

def main(file_path, force: bool = False):
    # run DB freshness check first
    try:
        up_to_date = check_db()
    except Exception as e:
        print(f"Warning: database check failed: {e}")
        up_to_date = None

    if up_to_date is False:
        print("Local hashes are out of date — updating now...")
        try:
            update_hashes_main(force=force)
            # re-run the check to confirm update succeeded
            try:
                up_to_date = check_db()
            except Exception:
                up_to_date = None

            if up_to_date:
                print("Local hashes updated successfully.")
            else:
                print("Update attempted but no new data detected, so assume new data propagation is lagging. Proceeding with existing data.")
        except Exception as e:
            print(f"Programmatic update failed: {e}")

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
        #call the file type detector and investigation modules here to do the actual analysis of the file.
        analysis_result = investigate_file(file_path)
        # add the analysis result to the verdict
        verdict = {
            "file_hash": file_hash,
            "known_malware": False,
            "detection_method": "No match in threat intelligence database",
            "analysis_result": analysis_result
        }

    print(json.dumps(verdict, indent=2))

if __name__ == "__main__":
    # usage: python main.py <file_path> [--force]
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python main.py <file_path> [--force]")
        sys.exit(1)

    force_flag = "--force" in sys.argv or "--force-update" in sys.argv
    file_arg = None
    for a in sys.argv[1:]:
        if a == "--force" or a == "--force-update":
            continue
        file_arg = a

    if not file_arg:
        print("Usage: python main.py <file_path> [--force]")
        sys.exit(1)

    main(file_arg, force=force_flag)
