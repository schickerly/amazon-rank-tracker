import streamlit as st
import requests
import base64
import json

st.title("🧪 DataForSEO Amazon Labs Test")

api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# ✅ Hardcoded payload
post_data = [
    {
        "language_name": "English",
        "amazon_domain": "amazon.com",
        "keyword": "vanilla soy candles highly scented",
        "depth": 100
    }
]

# ✅ Auth headers
auth_string = f"{api_login}:{api_password}"
b64_auth = base64.b64encode(auth_string.encode()).decode()
headers = {
    "Authorization": f"Basic {b64_auth}",
    "Content-Type": "application/json"
}

# ✅ Correct endpoint
url = "https://api.dataforseo.com/v3/dataforseo_labs/amazon/search_products/live"

# Run only when user clicks
if st.button("Run Test Request"):
    try:
        response = requests.post(url, headers=headers, json=post_data)
        data = response.json()
        st.subheader("Raw API Response:")
        st.json(data)

        # Safety check
        if not data.get("tasks"):
            st.error("⚠️ No 'tasks' in response. Confirm API access is enabled and funded.")
        else:
            st.success("✅ Request successful! You have task results.")
    except Exception as e:
        st.error(f"Request failed: {e}")
