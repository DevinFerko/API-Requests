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