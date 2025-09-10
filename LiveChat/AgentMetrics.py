#Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Opens Credentials file gets api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\CX Reporting\LiveChat\credentials.json") as f:
    creds = json.load(f)

API_TOKEN = creds["api_token"]

# Base URL for LiveChat API
BASE_URL = "https://api.livechatinc.com/v3.5/reports/agents/summary"

# Function to get agent metrics
def get_agent_metrics():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    # Add query parameters
    params = {
        "date_from": "2024-01-01",  
        "date_to": "2025-09-10"     
    }

    # Request data from LiveChat API
    response = requests.get(BASE_URL, headers=headers, params=params)

    # Check for successful response if not prints status code
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}, Response: {response.text}")
        return []
    
    data = response.json()
    total_chats_allAgents = sum(agent.get("total_chats", 0) for agent in data.get("agents", []))

    # Empty list to hold agent metrics
    agent_metrics = []

    # Process each agent's data - loops over each agent
    for agent in data.get("agents", []):
        total_chats = agent.get("total_chats", 0)
        percent_of_totalChats = (total_chats / total_chats_allAgents * 100) if total_chats_allAgents else 0
        metrics = {
            "Agent": agent.get("name"),
            "Total chats": total_chats,
            "% of all chats": round(percent_of_totalChats, 2),
            "Satisfaction": agent.get("satisfaction_rate"),
            "First response time": agent.get("first_response_time"),
            "Accepting time": agent.get("accepting_time"),
            "Not accepting time": agent.get("not_accepting_time"),
            "Logged in time": agent.get("logged_in_time"),
            "Chatting time": agent.get("chatting_time"),
            "Efficiency": agent.get("efficiency"),
            "Chats limit": agent.get("chats_limit")
        }

        agent_metrics.append(metrics)
    return agent_metrics


if __name__ == "__main__":
    agents = get_agent_metrics()
    for agent in agents:
        print(agent)
