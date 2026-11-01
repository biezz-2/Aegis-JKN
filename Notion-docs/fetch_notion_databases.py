import os
import requests
import json

token = os.getenv("NOTION_TOKEN", "")
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

dataset_db_id = "310b35a5-9346-42df-af47-df9897cdcda1"
claims_db_id = "c783afb3-d0d4-4582-9545-6180b7b7756b"

# Fetch dataset database with empty body
print("Fetching Dataset Database...")
dataset_response = requests.post(f"https://api.notion.com/v1/databases/{dataset_db_id}/query", headers=headers, json={})
with open("dataset_db.json", "w") as f:
    json.dump(dataset_response.json(), f, indent=2)
print(f"Dataset DB: {dataset_response.status_code}")
print(f"Results count: {len(dataset_response.json().get('results', []))}")

# Fetch claims database with empty body
print("Fetching Claims Database...")
claims_response = requests.post(f"https://api.notion.com/v1/databases/{claims_db_id}/query", headers=headers, json={})
with open("claims_db.json", "w") as f:
    json.dump(claims_response.json(), f, indent=2)
print(f"Claims DB: {claims_response.status_code}")
print(f"Results count: {len(claims_response.json().get('results', []))}")

print("\nAll databases saved!")
