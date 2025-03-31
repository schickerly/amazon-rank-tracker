import streamlit as st
import requests
import base64
import pandas as pd

st.title("Amazon Keyword Rank Checker")

# Inputs
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

asin = st.text_input("Your Product ASIN")
keywords = st.text_area("Enter Keywords (one per line)").splitlines()

if st.button("Check Rankings") and asin and keywords:
    st.write("Checking ranks...")
    results = []

    for kw in keywords:
        post_data = {
            "language_name": "English",
            "location_code": 2840,  # United States
            "keyword": kw,
            "depth": 100
        }
        auth_string = f"{api_login}:{api_password}"
        b64_auth = base64.b64encode(auth_string.encode()).decode()
        headers = {"Authorization": f"Basic {b64_auth}"}

        response = requests.post(
            "https://api.dataforseo.com/v3/amazon/products/search",
            json=[post_data],
            headers=headers
        )

        data = response.json()
        st.json(data)
        task = data.get('tasks', [])[0]

        if task.get('result'):
            keyword_results = task['result'][0].get('items', [])
        else:
            keyword_results = []

        # default to "-" if not found
        rank = "-"
        for i, item in enumerate(keyword_results):
            if item.get("asin") == asin:
                rank = i + 1
                break

        
        rank = "-"
        for i, item in enumerate(keyword_results):
            if item.get("asin") == asin:
                rank = i + 1
                break

        results.append({"Keyword": kw, "Rank": rank})

    df = pd.DataFrame(results)
    st.write(df)

    
