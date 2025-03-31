import streamlit as st
import requests
import base64
import json

st.title("🔥 Hardcoded Amazon Keyword Test")

# Pull credentials from Streamlit secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# Hardcoded keyword + settings
post_data = [{
    "language_name": "English",
    "amazon_domain": "amazon.com",
    "keyword": "vanilla soy candles highly scented",
    "depth": 100
}]

# Basic Auth
auth_string = f"{api_login}:{api_password}"
b64_auth = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/json"
}

# Make the API request
response = requests.post(
    "https://api.dataforseo.com/v3/dataforseo_labs/amazon/search_products/live",
    headers=headers,
    json=post_data
)

# Parse and show response
data = response.json()

# Pretty print the full API response
st.subheader("Raw API Response")
st.json(data)

# Show top results (if present)
task_list = data.get("tasks")
if not task_list:
    st.error("No data returned — check your API login, keyword, or credit balance.")
    st.stop()

items = task_list[0].get("result", [{}])[0].get("items", [])
if not items:
    st.warning("No products found in the search results.")
    st.stop()

st.subheader("Top Results (ASINs + Titles)")
for i, item in enumerate(items[:10], start=1):
    asin = item.get("asin", "N/A")
    title = item.get("title", "No Title")
    st.write(f"{i}. **{asin}** — {title}")
