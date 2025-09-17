import requests
import json
from datetime import datetime, timedelta

DOMAIN = "tapwarehouse.freshdesk.com"

# Opens crediential file reads api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\CX Reporting\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# BASE URL and Authentication
BASE_URL = f"https://{DOMAIN}/api/v2"
AUTH = (API_KEY, "X")  # Use API key as username, and 'X' as password placeholder

#Date Range
END_DATE = datetime.now()-timedelta(days=1) # Gets yesterday's date
START_DATE = END_DATE # Report on only one day (yesterday)

# Functions
# Generates a list of dates (YYYY-MM-DD) between start and end date.
def date_range(start_date, end_date):
    n_days = int((end_date - start_date).days)
    for n in range(n_days + 1):
        yield (start_date + timedelta(n)).strftime("%Y-%m-%d")

# Uses the search API to get the total count based on the query string.
def get_ticket_count(query):
    search_url = f"{BASE_URL}/search/tickets?query=\"{query}\""
    response = requests.get(search_url, auth=AUTH)
    # Checks for status code 200
    if response.status_code == 200:
        return int(response.headers.get("X-Total-Count", 0)) # Total count for search queries is in header
    else: 
        #Handles none 200 status codes
        print(f"  [API ERROR] Search Query Failed: {response.status_code} - {response.text[:50]}...")
        return 0