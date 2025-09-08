# Imports Libraries
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Get all agents
url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents" #Freshdesk URL

response = requests.get(url, auth=HTTPBasicAuth(API_KEY, "X"))

# Checks status code
if response.status_code == 200:
    agents = response.json()
    
    # Write to CSV
    with open("agents.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Header row
        writer.writerow(["ID", "Name", "Email"])
        
        # Data rows
        for agent in agents:
            writer.writerow([
                agent.get("id", ""),
                agent.get("contact", {}).get("name", "N/A"),
                agent.get("contact", {}).get("email", "N/A")
            ])
    
    print("✅ Agents exported to agents.csv")
else:
    print(f"Failed to fetch agents. Status Code: {response.status_code}, Response: {response.text}")