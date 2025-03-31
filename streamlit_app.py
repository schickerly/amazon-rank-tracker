import streamlit as st
import requests
import base64
import pandas as pd
import json

st.title("🔍 Amazon Keyword Rank Tracker (Debug Mode)")

# API credentials from secrets
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# Inputs
asin = st.text_input("Your Product ASIN")
keywords_raw = st.text_area("Enter keywords (one per line)")
keywords = [kw.strip() for kw in keywords_raw.splitlines() if kw.strip()]

if st.button("Check Rankings") and asin and keywords:
    st.info("📡 Sending requests... please wait.")
    results = []

    for kw in keywords:
        post_data = [{
            "keyword": kw,
            "language_name": "English",
            "amazon_domain": "amazon.com",
            "depth": 100
        }]

        # Auth header
        auth_string = f"{api_login}:{api_password}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()
        headers = {
            "Authorization": f"Basic {b64_auth}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.dataforseo.com/v3/amazon/products/search/live",
                headers=headers,
                json=post_data
            )

            data = response.json()

            st.subheader(f"📦 Raw API Response for '{kw}'")
            st.json(data)  # DEBUG: Show raw JSON so we can inspect it

            # Validate structure before trying to access results
            task_list = data.get("tasks")
            if not task_list:
                results.append({"Keyword": kw, "Rank": "No tasks returned"})
                continue

            task = task_list[0]
            result_list = task.get("result")
            if not result_list:
                results.append({"Keyword": kw, "Rank": "No results in task"})
                continue

            items = result_list[0].get("items", [])
            rank = "-"
            for i, item in enumerate(items):
                if item.get("asin") == asin:
                    rank = i + 1
                    break

            results.append({"Keyword": kw, "Rank": rank})
        
        except Exception as e:
            st.error(f"❌ Exception occurred: {e}")
            results.append({"Keyword": kw, "Rank": "Error"})

    df = pd.DataFrame(results)
    st.subheader("📊 Final Keyword Ranking Results")
    st.dataframe(df)
