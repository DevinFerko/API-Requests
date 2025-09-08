#Imports Libraries
import requests
from requests.auth import HTTPBasicAuth
import json

# Freshdesk domain and API key
FRESHDESK_DOMAIN = "tapwarehouse.freshdesk.com"

with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_KEY = creds["api_key"]

# Example: Get all agents
url = f"https://{FRESHDESK_DOMAIN}/api/v2/agents"

response = requests.get(url, auth=HTTPBasicAuth(API_KEY, "X"))

if response.status_code == 200:
    agents = response.json()
    for agent in agents:
        name = agent.get("contact", {}).get("name", "N/A")
        print(f"ID: {agent['id']}, Name: {name}")
else:
    print(f"Failed to fetch agents. Status Code: {response.status_code}, Response: {response.text}")
