import streamlit as st
import requests

st.set_page_config(page_title="Bible Study Helper", page_icon="📖")

st.title("📖 Scripture Finder")
st.subheader("Find verses by topic or keyword")

# User Input
topic = st.text_input("Enter a topic (e.g., Faith, Hope, Love):", "")

if topic:
    # We use a public API to fetch verses based on the keyword
    # Note: Many Bible APIs work best with direct references, 
    # but we can simulate a topic search here.
    api_url = f"https://bible-api.com/{topic}" 
    
    with st.spinner('Searching the Word...'):
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            st.success(f"Found verses related to: {topic}")
            st.write(f"**{data['reference']}**")
            st.write(data['text'])
        else:
            st.warning("Could not find a direct match. Try a specific reference or a different keyword.")

st.info("Tip: Use this to find text for your next sermon video or album art!")