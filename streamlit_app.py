import streamlit as st
import requests
import base64
import pandas as pd
import json

st.title("🔍 Amazon Ranked Keywords (DataForSEO Labs)")

# Load credentials from secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# User inputs
asin = st.text_input("Enter your Amazon ASIN", value="019005476X")
limit = st.slider("Number of keywords to return", 1, 100, 10)

if st.button("Fetch Ranked Keywords") and asin:
    st.info("Fetching ranked keywords from DataForSEO Labs...")

    # Build the POST payload
    post_data = [
        {
            "asin": asin,
            "location_code": 2840,
            "language_code": "en",
            "ignore_synonyms": False,
            "limit": limit
        }
    ]

    # Auth headers
    auth_string = f"{api_login}:{api_password}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/json"
    }

    try:
        # Make the request using 'data' not 'json' (required by this endpoint!)
        response = requests.post(
            "https://api.dataforseo.com/v3/dataforseo_labs/amazon/ranked_keywords/live",
            headers=headers,
            data=json.dumps(post_data)
        )

        data = response.json()
        st.subheader("📦 Raw API Response")
        st.json(data)

        task_list = data.get("tasks")
        if not task_list:
            st.error("No tasks returned. This may mean your account isn’t yet approved for Labs.")
            st.stop()

        result_items = task_list[0].get("result", [{}])[0].get("items", [])
        keywords = []

        for item in result_items:
            kw = item.get("keyword_data", {}).get("keyword", "N/A")
            rank = item.get("rank_group", "N/A")
            keywords.append({"Keyword": kw, "Rank Group": rank})

        df = pd.DataFrame(keywords)
        st.subheader("📊 Top Ranked Keywords")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error: {e}")
