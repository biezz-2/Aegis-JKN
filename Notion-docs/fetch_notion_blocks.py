import os
import requests
import json

token = os.getenv("NOTION_TOKEN", "")
page_id = "3f23e603-1ab7-808d-b2cb-fe92cd62391d"

headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

# Get page blocks
response = requests.get(f"https://api.notion.com/v1/blocks/{page_id}/children", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
    # Save to file
    with open("notion_blocks.json", "w") as f:
        json.dump(data, f, indent=2)
    print("\nSaved to notion_blocks.json")
else:
    print(f"Error: {response.text}")
