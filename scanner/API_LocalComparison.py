from getRecentAPIData import get_latest_sample_timestamp
from localHashes_Check import last_modified
from datetime import datetime
import os
import json

def _parse_ts(s: str):
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def main() -> bool:
    """Return True if local DB is up to date; prints status.

    This treats the local CSV's newest `first_seen` as up-to-date when it is
    equal to or newer than the API's latest sample timestamp.
    """
    latest = get_latest_sample_timestamp()

    print("API latest sample timestamp:", latest)
    print("Local CSV newest first_seen:", last_modified)

    latest_dt = _parse_ts(latest) if latest else None
    local_dt = _parse_ts(last_modified) if last_modified else None

    # Check metadata (written after successful import) as an authoritative signal
    try:
        metadata_path = os.path.join(os.path.dirname(__file__), "data", "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as mf:
                meta = json.load(mf)
            meta_ts = _parse_ts(meta.get("last_api_timestamp"))
            if meta_ts and latest_dt and meta_ts >= latest_dt:
                print("Database is up to date (metadata).")
                return True
    except Exception:
        # metadata read failure should not break the check; fall back to CSV comparison
        pass

    if latest_dt and local_dt:
        if local_dt >= latest_dt:
            print("Database is up to date")
            return True
        else:
            print("Database needs to be updated!")
            return False
    else:
        # fallback to previous exact-string comparison when parsing fails
        if latest == last_modified:
            print("Database is up to date")
            return True
        else:
            print("Database needs to be updated!")
            return False


if __name__ == "__main__":
    main()