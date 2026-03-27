import requests
from dotenv import load_dotenv
import os
load_dotenv()
base_url = os.getenv("BASE_URL")
API_URL = f"{base_url}/admin/v2/alerts"


async def get_headers(token: str, headers: dict | None = None) -> dict:
    # Get the token from the active MCP request context
    base_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    if headers:
        base_headers.update(headers)

    return base_headers


async def get_alert_list(token: str):
    url = f"{API_URL}/list"
    payload = {"status": "ACTIVE"}
    response = requests.post(url, json=payload, headers=await get_headers(token))
    return response.text


async def get_alert(id: str, token: str):
    url = f"{API_URL}/{id}"
    response = requests.get(url, headers=await get_headers(token))
    return response.text


async def create_alert(payload: any, token: str):
    url = f"{API_URL}"
    response = requests.post(url, json=payload, headers=await get_headers(token))
    return response.text
