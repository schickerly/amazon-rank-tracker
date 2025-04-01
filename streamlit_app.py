import streamlit as st
import requests
import base64
import pandas as pd
import json

st.title("📈 Amazon Ranked Keywords via DataForSEO Labs")

# Streamlit secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# Inputs
asin = st.text_input("Enter your Amazon ASIN", value="B01G3SP5ZM")
limit = st.slider("How many top keywords do you want to see?", min_value=1, max_value=100, value=10)

if st.button("Fetch Ranked Keywords") and asin:
    st.info(f"📡 Fetching ranked keywords for ASIN: {asin}...")

    # Payload
    post_data = [
        {
            "asin": asin,
            "location_code": 2840,
            "language_code": "en",
            "ignore_synonyms": False,
            "limit": limit
        }
    ]

    # Headers
    auth_string = f"{api_login}:{api_password}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            "https://api.dataforseo.com/v3/dataforseo_labs/amazon/ranked_keywords/live",
            headers=headers,
            data=json.dumps(post_data)
        )

        data = response.json()

        st.subheader("📦 Raw API Response")
        st.json(data)

        task_list = data.get("tasks", [])
        if not task_list or task_list[0].get("result") is None:
            st.error("No results returned. Please check the ASIN or try again.")
            st.stop()

        result_items = task_list[0]["result"][0].get("items", [])

        rows = []
        for item in result_items:
            kw = item.get("keyword_data", {}).get("keyword", "N/A")
            vol = item.get("keyword_data", {}).get("keyword_info", {}).get("search_volume", "N/A")
            rank = item.get("ranked_serp_element", {}).get("serp_item", {}).get("rank_group", "N/A")
            rows.append({
                "Keyword": kw,
                "Search Volume": vol,
                "Rank Group": rank
            })

        df = pd.DataFrame(rows)
        st.subheader("📊 Keyword Rankings")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")
