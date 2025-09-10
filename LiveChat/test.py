#Imports Library
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

# Freshdesk domain and API key
LIVECHAT_DOMAIN = ""

# Opens Credentials file gets api key
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

API_TOKEN = creds["api_token"]