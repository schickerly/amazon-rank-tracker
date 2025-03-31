import streamlit as st
import requests
import base64
import pandas as pd

st.title("Amazon Keyword Rank Checker (MVP)")

# Get API credentials from secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# User inputs
asin = st.text_input("Your Product ASIN")
keywords_raw = st.text_area("Enter Keywords (one per line)")
keywords = [k.strip() for k in keywords_raw.splitlines() if k.strip()]

if st.button("Check Rankings") and asin and keywords:
    st.write("Checking ranks...")
    results = []

    for kw in keywords:
        post_data = {
            "language_name": "English",
            "amazon_domain": "amazon.com",  # US marketplace
            "keyword": kw,
            "depth": 100
        }

        # Basic Auth
        auth_string = f"{api_login}:{api_password}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()
        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json"
        }

        # Correct endpoint for Amazon product search
        response = requests.post(
            "https://api.dataforseo.com/v3/dataforseo_labs/amazon/search_products/live",
            headers=headers,
            json=[post_data]
        )

        data = response.json()
        # Debug raw output
        # st.json(data)

        # Safely handle response
        task = data.get('tasks', [{}])[0]
        keyword_results = task.get('result', [{}])[0].get('items', [])

        rank = "-"
        for i, item in enumerate(keyword_results):
            if item.get("asin") == asin:
                rank = i + 1
                break

        results.append({"Keyword": kw, "Rank": rank})

    df = pd.DataFrame(results)
    st.subheader("Keyword Rankings:")
    st.dataframe(df)
