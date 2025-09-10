#Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
LIVECHAT_DOMAIN = ""

# Opens Credentials file gets api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\CX Reporting\LiveChat\credentials.json") as f:
    creds = json.load(f)

API_TOKEN = creds["api_token"]

BASE_URL = "https://api.livechatinc.com/v3.5/reports/agents"

agent_metrics = []

def get_agent_metrics():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # You can add query parameters, e.g., date range
    params = {
        "date_from": "2024-01-01",  # adjust as needed
        "date_to": "2025-09-10"     # adjust as needed
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}, Response: {response.text}")
        return []
    return response.json().get("data", [])