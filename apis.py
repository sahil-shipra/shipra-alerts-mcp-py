import requests


async def get_headers(headers: dict | None = None) -> dict:
    base_headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY4ODU3OTI2NWFhOTBiZTIwOTk4ZDdmOSIsInNlc3Npb25JZCI6IjY5YzUwYWRhOTQ0MTEyNGVhM2ZkNTgyZCIsImZObSI6IlNhaGlsIiwibE5tIjoiUGF0ZWwgRGV2IiwiZW1haWwiOiJzYWhpbEBzaGlwcmEuY2EiLCJpYXQiOjE3NzQ1MjEwNTAsImV4cCI6MTc3NzE0OTA1MH0.sIC045mbjlJTnplmBeQ4cjZTd1-HgA6tF9dIs2-LGBw",
        "Content-Type": "application/json",
    }

    if headers:
        base_headers.update(headers)

    return base_headers

BASE_URL = "http://localhost:3007/admin/v2/alerts"


async def get_alert_list():
    url = f"{BASE_URL}/list"
    payload = {"status": "ACTIVE"}
    response = requests.post(url, json=payload, headers=await get_headers())
    return response.text


async def get_alert(id: str):
    url = f"{BASE_URL}/{id}"
    response = requests.get(url, headers=await get_headers())
    return response.text


async def create_alert(payload: any):
    url = f"{BASE_URL}"
    response = requests.post(url, json=payload, headers=await get_headers())
    return response.text
