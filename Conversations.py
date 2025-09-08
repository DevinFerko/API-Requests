#Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Base URL + conversation url
url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"
con_url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets{ticket.id}/conversations"

all_tickets = []
page = 1
per_page = 100  # Freshdesk allows up to 100 per page

while True:
    response = requests.get(
        url,
        auth=HTTPBasicAuth(API_KEY, "X"),
        params={"page": page, "per_page": per_page} 
    )

    if response.status_code != 200:
        print(f"❌ Failed on page {page}. Status Code: {response.status_code}, Response: {response.text}")
        break

    tickets = response.json()
