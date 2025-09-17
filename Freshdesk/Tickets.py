#Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

# Opens Credentials file gets api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\CX Reporting\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Base URL
url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"

all_tickets = [] #empty array
page = 1
per_page = 100  # Freshdesk allows up to 100 per page

while True:
    response = requests.get(
        url,
        auth=HTTPBasicAuth(API_KEY, "X"),
        params={"page": page, "per_page": per_page}
    )

    # Ensures status code is 200
    if response.status_code != 200:
        print(f"Failed on page {page}. Status Code: {response.status_code}, Response: {response.text}")
        break

    # Tickets as response
    tickets = response.json()

    if not tickets:  # No more tickets
        break

    all_tickets.extend(tickets)
    #print(f"Fetched page {page}, tickets so far: {len(all_tickets)}")
    page += 1

# Write to CSV
with open("tickets.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Agent Id", "Status", "Updated"])  # Header row

    for ticket in all_tickets:
        writer.writerow([
            ticket.get("id", ""),
            ticket.get("responder_id", ""),
            ticket.get("status", ""),
            ticket.get("updated_at", "") 
        ])

print(f"Export complete! Total tickets: {len(all_tickets)}")