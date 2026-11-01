import os
import requests

token = os.getenv("NOTION_TOKEN", "")
headers = {
    "Authorization": f"Bearer {token}",
    "Notion-Version": "2022-06-28"
}

response = requests.get("https://api.notion.com/v1/users/me", headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
