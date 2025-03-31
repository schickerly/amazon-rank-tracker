import streamlit as st
import requests
import base64
import pandas as pd

st.title("🔍 Amazon Top Ranked Keywords for ASIN")

# Get credentials
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# ASIN input
asin = st.text_input("Enter your Amazon ASIN")
limit = st.slider("How many keywords to return?", 1, 50, 10)

if st.button("Get Ranked Keywords") and asin:
    st.info("📡 Fetching ranked keywords...")

    # Build payload
    post_data = [
        {
            "asin": asin,
            "location_code": 2840,  # United States
            "language_code": "en",
            "limit": limit,
            "order_by": ["keyword_data.keyword,asc"]
        }
    ]

    # Encode API credentials
    auth_string = f"{api_login}:{api_password}"
    b64_auth = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_auth}",
        "Content-Type": "application/json"
    }

    # Make request
    try:
        response = requests.post(
            "https://api.dataforseo.com/v3/amazon/ranked_keywords/live",
            headers=headers,
            json=post_data
        )

        data = response.json()
        st.subheader("📦 Raw API Response")
        st.json(data)

        task = data.get("tasks", [{}])[0]
        result_list = task.get("result", [{}])[0].get("items", [])

        # Parse results into table
        keywords = []
        for item in result_list:
            kw = item.get("keyword_data", {}).get("keyword", "N/A")
            pos = item.get("ranked_serp_element", {}).get("position", "N/A")
            keywords.append({"Keyword": kw, "Position": pos})

        df = pd.DataFrame(keywords)
        st.subheader("📊 Top Ranked Keywords")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")
