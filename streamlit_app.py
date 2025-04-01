from client import RestClient
import streamlit as st

st.title("🔍 DataForSEO Labs Ranked Keywords Test")

api_login = st.secrets["dataforseo"]["api_login"]
api_password = st.secrets["dataforseo"]["api_password"]

if st.button("Run Test"):
    client = RestClient(api_login, api_password)

    post_data = dict()
    post_data[len(post_data)] = dict(
        asin="B00R92CL5E",  # known good ASIN
        location_name="United States",
        language_name="English"
    )

    response = client.post("/v3/dataforseo_labs/amazon/ranked_keywords/live", post_data)

    if response["status_code"] == 20000:
        st.success("✅ Success!")
        st.json(response)
    else:
        st.error(f"❌ Error {response['status_code']}: {response['status_message']}")
