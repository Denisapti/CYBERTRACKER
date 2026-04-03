import sys
import json
from db_init import ensure_user_db_exists
from hashing import sha256_file
from db import check_hash
from API_LocalComparison import main as check_db
from file_type_detector import investigate_file
from update_hashes import main as update_hashes_main
from ui import show_scan_result, show_error

def main(file_path, force: bool = False, cli_mode: bool = False):
    # Ensure database is initialized before any operations
    ensure_user_db_exists()
    
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
            "file_path": file_path,
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
            "file_path": file_path,
            "file_hash": file_hash,
            "known_malware": False,
            "detection_method": "No match in threat intelligence database",
            "analysis_result": analysis_result
        }

    print(json.dumps(verdict, indent=2))
    
    # Also show GUI popup if not in CLI mode
    if not cli_mode:
        try:
            show_scan_result(verdict)
        except Exception as e:
            print(f"Warning: UI display failed: {e}")

if __name__ == "__main__":
    # usage: python main.py <file_path> [--force] [--cli]
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print("Usage: python main.py <file_path> [--force] [--cli]")
        sys.exit(1)

    force_flag = "--force" in sys.argv or "--force-update" in sys.argv
    cli_flag = "--cli" in sys.argv
    file_arg = None
    for a in sys.argv[1:]:
        if a == "--force" or a == "--force-update" or a == "--cli":
            continue
        file_arg = a

    if not file_arg:
        print("Usage: python main.py <file_path> [--force] [--cli]")
        sys.exit(1)

    try:
        main(file_arg, force=force_flag, cli_mode=cli_flag)
    except Exception as e:
        error_msg = f"Scan failed: {str(e)}"
        print(f"Error: {error_msg}", file=sys.stderr)
        try:
            show_error(error_msg)
        except:
            pass  # UI not available, just continue
        sys.exit(1)
