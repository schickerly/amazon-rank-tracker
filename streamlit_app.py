import streamlit as st
import requests
import base64
import pandas as pd
import json

st.title("📈 Amazon Ranked Keywords via DataForSEO Labs")

# Load credentials
api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

# ASIN input
asin = st.text_input("Enter your Amazon ASIN", value="B01G3SP5ZM")

if st.button("Fetch Ranked Keywords") and asin:
    st.info(f"📡 Fetching up to 1000 ranked keywords for ASIN: {asin}...")

    # Request body
    post_data = [
        {
            "asin": asin,
            "location_code": 2840,
            "language_code": "en",
            "ignore_synonyms": False,
            "limit": 1000
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
        response = requests.post(
            "https://api.dataforseo.com/v3/dataforseo_labs/amazon/ranked_keywords/live",
            headers=headers,
            data=json.dumps(post_data)
        )

        data = response.json()
        st.subheader("📦 Raw API Response")
        st.json(data)

        task_list = data.get("tasks", [])
        if not task_list:
            st.error("❌ No task returned.")
            st.stop()

        result = task_list[0].get("result", [])
        if not result or not result[0].get("items"):
            st.warning("No keyword rankings found.")
            st.stop()

        result_items = result[0]["items"]

        # 🔥 Grab item summary info from first result
        first_item = result_items[0].get("ranked_serp_element", {}).get("serp_item", {})
        item_title = first_item.get("title", "N/A")
        item_price = first_item.get("price_from", "N/A")
        item_rating = first_item.get("rating", {}).get("value", "N/A")
        item_reviews = first_item.get("rating", {}).get("votes_count", "N/A")
        item_asin = first_item.get("asin", "N/A")

        st.markdown(f"""
        ### 🕯️ Product Overview
        **Title:** {item_title}  
        **ASIN:** `{item_asin}`  
        **Price:** ${item_price}  
        **Rating:** ⭐ {item_rating} ({item_reviews} reviews)
        """)

        # Build and filter rows
        rows = []
        for item in result_items:
            kw = item.get("keyword_data", {}).get("keyword", "N/A")
            vol = item.get("keyword_data", {}).get("keyword_info", {}).get("search_volume", 0)
            rank = item.get("ranked_serp_element", {}).get("serp_item", {}).get("rank_group", "N/A")
            is_choice = item.get("ranked_serp_element", {}).get("serp_item", {}).get("is_amazon_choice", False)
            is_best = item.get("ranked_serp_element", {}).get("serp_item", {}).get("is_best_seller", False)

            rows.append({
                "Keyword": kw,
                "Search Volume": vol,
                "Rank": rank,
                "Amazon Choice": "✅" if is_choice else "❌",
                "Best Seller": "✅" if is_best else "❌"
            })

        df = pd.DataFrame(rows)

        # Sort by search volume descending
        df = df.sort_values(by="Search Volume", ascending=False)

        st.subheader("📊 Top Ranked Keywords")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")
