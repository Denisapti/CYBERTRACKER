import requests
from datetime import datetime

API_URL = "https://mb-api.abuse.ch/api/v1/"
API_KEY = "adc7c0f7a891ecac5b5302f3313ef888d76cff355cc442df"  # Put your actual Auth-Key here

def get_latest_sample_timestamp():
    
    #Queries MalwareBazaar API for recent samples and returns
    #the timestamp of the most recent sample added.
    

    headers = {
        "Auth-Key": API_KEY
    }

    data = {
        "query": "get_recent",
        "selector": "time"  # sorts the data with the newesst first 
    }

    try:
        response = requests.post(API_URL, headers=headers, data=data)
        response.raise_for_status()
        json_data = response.json()

        if json_data.get("query_status") != "ok": #json_data is just the reply from the API
            print("API query failed or no new results")
            return None

        recent_samples = json_data.get("data", [])
        if not recent_samples:
            return None

       
        timestamps = [item["first_seen"] for item in recent_samples if "first_seen" in item] 
        datetime_stamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamps]

      
        newest_dt = max(datetime_stamps) # finding the newest date
        
        return newest_dt.strftime("%Y-%m-%d %H:%M:%S") #turns baCK INTO a string


    except Exception as e:
        print(f"Error querying MalwareBazaar with API key: {e}")
        return None