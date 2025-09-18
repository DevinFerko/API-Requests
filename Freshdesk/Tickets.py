# Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

# Opens Credentials file gets api key
# NOTE: Assuming this path and file exist and are correct
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\CX Reporting\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Base URL
url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"

all_tickets = [] #empty array
page = 1
per_page = 100 

# --------------------------
# RECOMMENDED FIX PARAMETERS
# --------------------------
# 1. Order by 'created_at' to ensure stable, non-shifting pagination.
# 2. You can also add a 'created_since' filter to only get recent tickets.
params = {
    "per_page": per_page,
    "order_by": "created_at",
    "order_type": "asc" # or "desc", depending on your preference
}

print("Starting ticket retrieval...")

while True:
    params["page"] = page # Update the page number in the parameters

    response = requests.get(
        url,
        auth=HTTPBasicAuth(API_KEY, "X"),
        params=params
    )

    # Ensures status code is 200
    if response.status_code != 200:
        # Check for 429 Rate Limit error, implement retry logic if needed
        if response.status_code == 429:
            print(f"[ERROR] Rate limit exceeded on page {page}. Waiting and retrying...")
            
            # Wait before retrying - (optional) 
            #retry_after = int(response.headers.get("Retry-After", 60)) # Default to 60 seconds if not provided
            #time.sleep(retry_after)
        else:
            print(f"Failed on page {page}. Status Code: {response.status_code}, Response: {response.text}")
            break
        break # Exit on general error

    # Tickets as response
    try:
        tickets = response.json()
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to decode JSON response on page {page}. Response: {response.text[:100]}...")
        break

    if not tickets: # No more tickets
        print(f"Reached end of tickets on page {page}.")
        break

    all_tickets.extend(tickets)

    # Debugging output (optional)
    #print(f"Fetched page {page}. Total tickets so far: {len(all_tickets)}")
    page += 1

# Write to CSV
try:
    with open("tickets.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Agent Id", "Status", "Updated"]) # Header row

        for ticket in all_tickets:
            writer.writerow([
                ticket.get("id", ""),
                ticket.get("responder_id", ""),
                ticket.get("status", ""),
                # Freshdesk status codes are numbers, e.g., 2=Open, 4=Resolved
                # To make this human-readable, you might want to map the status code here.
                ticket.get("updated_at", "") 
            ])
except Exception as e:
    print(f"[ERROR] Failed to write to CSV: {e}")

print(f"Export complete! Total tickets: {len(all_tickets)}")