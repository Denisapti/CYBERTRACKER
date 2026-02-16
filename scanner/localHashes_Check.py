import os
from datetime import datetime

file_path = "/workspaces/CYBERTRACKER/scanner/data/hashes.csv"  


mod_timestamp = os.path.getmtime(file_path)


last_modified = datetime.fromtimestamp(mod_timestamp).strftime("%Y-%m-%d %H:%M:%S")

print("The local hashes file was last modified on:", last_modified)