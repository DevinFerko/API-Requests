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

all_tickets = []
page = 1
per_page = 100  # Freshdesk allows up to 100 per page

# Loop through each page of tickets
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
    if not tickets:  # No more tickets
        break

    for ticket in tickets:
        ticket_id = ticket["id"]
        con_url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets/{ticket_id}/conversations"

        con_response = requests.get(
            con_url,
            auth=HTTPBasicAuth(API_KEY, "X")
        )

        if con_response.status_code == 200:
            conversations = con_response.json()
            replies = [conv for conv in conversations if not conv.get("private", False)]

            ticket_data = {
                "ticket_id": ticket_id,
                "subject": ticket.get("subject", ""),
                "status": ticket.get("status"),
                "priority": ticket.get("priority"),
                "responder_id": ticket.get("responder_id"),
                "num_replies": len(replies)
            }

            all_tickets.append(ticket_data)
        else:
            print(f"⚠️ Could not fetch conversations for ticket {ticket_id}. "
                  f"Status: {con_response.status_code}, Response: {con_response.text}")

    page += 1  # Move to next page

# Write to CSV
with open("tickets2.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Ticket ID", "Agent Id", "Status", "Subject", "Priority", "Num Replies"])  # Header row

    for ticket in all_tickets:
        writer.writerow([
            ticket.get("ticket_id", ""),
            ticket.get("responder_id", ""),
            ticket.get("status", ""),
            ticket.get("subject", ""),
            ticket.get("priority", ""),
            ticket.get("num_replies", 0)
        ])

print(f"🎉 Export complete! Total tickets: {len(all_tickets)}")
