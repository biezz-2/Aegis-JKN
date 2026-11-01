import os
import requests
import json

token = os.getenv("NOTION_TOKEN", "")
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

# Get all pages and databases
main_page_id = "3f23e603-1ab7-808d-b2cb-fe92cd62391d"

# IDs from blocks
architecture_page_id = "3ef3e603-1ab7-81d1-962a-f8955843ed0f"
simulation_page_id = "3f23e603-1ab7-81bf-99a7-d3f1768f1708"
dataset_db_id = "310b35a5-9346-42df-af47-df9897cdcda1"
claims_db_id = "c783afb3-d0d4-4582-9545-6180b7b7756b"

# Fetch architecture page blocks
print("Fetching Architecture Page...")
arch_response = requests.get(f"https://api.notion.com/v1/blocks/{architecture_page_id}/children", headers=headers)
with open("architecture_blocks.json", "w") as f:
    json.dump(arch_response.json(), f, indent=2)
print(f"Architecture: {arch_response.status_code}")

# Fetch simulation page blocks
print("Fetching Simulation Page...")
sim_response = requests.get(f"https://api.notion.com/v1/blocks/{simulation_page_id}/children", headers=headers)
with open("simulation_blocks.json", "w") as f:
    json.dump(sim_response.json(), f, indent=2)
print(f"Simulation: {sim_response.status_code}")

# Fetch dataset database
print("Fetching Dataset Database...")
dataset_response = requests.get(f"https://api.notion.com/v1/databases/{dataset_db_id}/query", headers=headers)
with open("dataset_db.json", "w") as f:
    json.dump(dataset_response.json(), f, indent=2)
print(f"Dataset DB: {dataset_response.status_code}")

# Fetch claims database
print("Fetching Claims Database...")
claims_response = requests.get(f"https://api.notion.com/v1/databases/{claims_db_id}/query", headers=headers)
with open("claims_db.json", "w") as f:
    json.dump(claims_response.json(), f, indent=2)
print(f"Claims DB: {claims_response.status_code}")

print("\nAll content saved!")
