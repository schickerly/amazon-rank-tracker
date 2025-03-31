import streamlit as st
import requests
import base64
import pandas as pd

st.title("🔍 Amazon Keyword Rank Tracker")

# API credentials from Streamlit secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# User inputs
asin = st.text_input("Your Product ASIN")
keywords_raw = st.text_area("Enter keywords (one per line)")
keywords = [kw.strip() for kw in keywords_raw.splitlines() if kw.strip()]

if st.button("Check Rankings") and asin and keywords:
    st.write("🔄 Checking keyword rankings...")
    results = []

    for kw in keywords:
        # Build request payload
        post_data = [{
            "keyword": kw,
            "language_name": "English",
            "amazon_domain": "amazon.com",
            "depth": 100
        }]

        # Encode API credentials for Basic Auth
        auth_string = f"{api_login}:{api_password}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()
        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json"
        }

        # Send request to correct Amazon SERP API endpoint
        response = requests.post(
            "https://api.dataforseo.com/v3/amazon/products/search/live",
            headers=headers,
            json=post_data
        )

        # Parse the response
        data = response.json()

        task = data.get("tasks", [{}])[0]
        result_list = task.get("result", [{}])
        if not result_list:
            results.append({"Keyword": kw, "Rank": "No results"})
            continue

        items = result_list[0].get("items", [])

        # Find your ASIN in the results
        rank = "-"
        for i, item in enumerate(items):
            if item.get("asin") == asin:
                rank = i + 1
                break

        results.append({"Keyword": kw, "Rank": rank})

    # Show results
    df = pd.DataFrame(results)
    st.subheader("📊 Keyword Rankings")
    st.dataframe(df)
