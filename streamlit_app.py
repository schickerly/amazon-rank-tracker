import requests
import base64
import json

# API credentials
api_login = "your_login"
api_password = "your_password"

# Payload: simple test keyword
post_data = [
    {
        "language_name": "English",
        "amazon_domain": "amazon.com",
        "keyword": "vanilla soy candles highly scented",
        "depth": 100
    }
]

# Headers with base64 auth
auth_string = f"{api_login}:{api_password}"
b64_auth = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/json"
}

# ✅ Double-confirmed endpoint
url = "https://api.dataforseo.com/v3/dataforseo_labs/amazon/search_products/live"

# Make request
response = requests.post(url, headers=headers, json=post_data)

# Print results
print(json.dumps(response.json(), indent=2))
