import requests
import json

# Absolute path to credentials file
with open(r"C:\Users\Devin Ferko\Desktop\Codes\API Requests\Freshdesk\credentials.json") as f:
    creds = json.load(f)

api_key = creds["api_key"]
domain = creds["domain"]
password = creds["password"]

url = f"https://{domain}/api/v2/tickets?filter=new_and_my_open"

r = requests.get(url, auth=(api_key, password))

if r.status_code == 200:
    print("Request processed successfully, the response is given below:")
    print(json.dumps(r.json(), indent=2))
else:
    print("Failed to read tickets, errors are displayed below:")
    try:
        response = r.json()
        print(response.get("errors", response))
    except json.JSONDecodeError:
        print(r.text)

    print("x-request-id :", r.headers.get("x-request-id", "N/A"))
    print("Status Code :", r.status_code)
