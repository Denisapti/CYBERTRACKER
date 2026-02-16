from getRecentAPIData import get_latest_sample_timestamp
from localHashes_Check import last_modified

latest = get_latest_sample_timestamp()
print ("Database was last updated at:", latest)
if latest == last_modified:
    print("Database is up to date")
    
else:
    print("Database needs to be updated!")

    # osama's code will follow here, not sure what to add here in place of that so i just used print statements