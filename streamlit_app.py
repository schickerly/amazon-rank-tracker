from client import RestClient

# Use your actual DataForSEO credentials here
client = RestClient("your_login", "your_password")

# Prepare request data
post_data = dict()
post_data[len(post_data)] = dict(
    asin="B01G3SP5ZM",             # A known valid ASIN
    location_name="United States",
    language_name="English"
)

# Make the API call
response = client.post("/v3/dataforseo_labs/amazon/ranked_keywords/live", post_data)

# Show results
if response["status_code"] == 20000:
    print("✅ Success!")
    print(response)
else:
    print(f"❌ Error. Code: {response['status_code']} - Message: {response['status_message']}")
