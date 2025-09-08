# Imports Libraries
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

# Opens crediential file reads api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Get all agents
url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents" #Freshdesk URL

all_agents = []
page = 1 # Starts at page 1
per_page = 100 # 100 rows per page, Freshdesk max

# Begin while true
while True:
    response = requests.get(url, auth=HTTPBasicAuth(API_KEY, "X"), params={"page": page, "per_page": per_page})

    # Break if not code 200
    if response.status_code != 200:
        print(f"failed on page {page}, Status Code: {response.status_code}, Response: {response.text} ")
        break

    agents = response.json()

    if not agents:
        break

    all_agents.extend(agents)

# writes agents csv
with open("agents.csv", mode="w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["ID", "Name", "Email"]) #Header Row
        
    # Data rows
    for agent in all_agents:
        writer.writerow([
            agent.get("id", ""),
            agent.get("contact", {}).get("name", "N/A"),
            agent.get("contact", {}).get("email", "N/A")
        ])

print(f"Export complete - Total Agents: {len(all_agents)}")