import os
import requests
import json

token = os.getenv("NOTION_TOKEN", "")
# Page ID dari URL: HEALTHKATHON-3f23e6031ab7808db2cbfe92cd62391d
page_id = "3f23e603-1ab7-808d-b2cb-fe92cd62391d"

headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

# Get page content
response = requests.get(f"https://api.notion.com/v1/pages/{page_id}", headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2))
else:
    print(f"Error: {response.text}")
