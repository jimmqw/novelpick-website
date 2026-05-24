import requests
import json

url = "https://api.302.ai/v1/images/generations"
# Try different endpoints
endpoints = [
    "https://api.302.ai/v1/images/generations",
    "https://api.302.ai/images/v1/generations",
    "https://api.302.ai/v1/images",
]
for url in endpoints:
    print(f"Trying: {url}")
headers = {
    "Authorization": "Bearer sk-m8Nlf73UMzo90eW2qZGWtjL2PpQw3NJseXQpKMODUowVTaPO",
    "Content-Type": "application/json"
}
data = {
    "model": "gpt-image-2",
    "prompt": "A beautiful anime girl",
    "n": 1,
    "size": "1024x1024"
}

try:
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    print(f"Status: {resp.status_code}")
    print(f"Response: {resp.text[:1000]}")
except Exception as e:
    print(f"Error: {e}")
