import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TCRRA Bible Hub", page_icon="📖", layout="wide")

# --- 2. RELIABLE API FUNCTIONS ---

def get_verse_of_the_day():
    """Fetches the live daily verse from OurManna (No Key Needed)"""
    try:
        url = "https://beta.ourmanna.com/api/v1/get?format=json&order=daily"
        response = requests.get(url, timeout=5).json()
        return {
            "text": response['verse']['details']['text'],
            "ref": response['verse']['details']['reference']
        }
    except:
        # High-quality fallback if the web service is down
        return {"text": "For I know the plans I have for you, declares the Lord.", "ref": "Jeremiah 29:11"}

def search_bible_topic(query, translation):
    """Searches for verses by keyword or reference using Bible-API"""
    # Bible-API is extremely fast and handles keywords well
    url = f"https://bible-api.com/{query}?translation={translation.lower()}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# --- 3. MODERN USER INTERFACE ---

st.title("📖 Bible Study & Sermon Hub")
st.write("A clean, reliable tool for your ministry and study.")

# --- Verse of the Day Card ---
votd = get_verse_of_the_day()
st.info(f"🌟 **Verse of the Day**\n\n\"{votd['text']}\"\n\n— **{votd['ref']}**")

st.divider()

# --- Search Section ---
col_side, col_main = st.columns([1, 2])

with col_side:
    st.subheader("Settings")
    # Standard translations supported by this API
    translation_options = {
        "King James Version": "kjv",
        "World English Bible": "web",
        "American Standard Version": "asv",
        "Bible in Basic English": "bbe"
    }
    selected_ver = st.selectbox("Choose Translation", list(translation_options.keys()))
    ver_code = translation_options[selected_ver]
    
    st.markdown("---")
    st.caption("Tip: Type a keyword like 'Healing' or a specific verse like 'John 3:16'")

with col_main:
    st.subheader("🔍 Search the Word")
    user_query = st.text_input("What are you studying today?", placeholder="Enter topic or verse...")

    if user_query:
        with st.spinner('Searching the database...'):
            data = search_bible_topic(user_query, ver_code)
            
            if data and 'text' in data:
                st.success(f"Results for '{user_query}' ({selected_ver})")
                
                # Displaying the result in a clean, readable box
                st.markdown(f"### {data['reference']}")
                st.markdown(f"> {data['text']}")
                
                # Copy button logic
                st.button("📋 Ready to Copy for Sermon")
            else:
                st.error("We couldn't find a match for that. Try a simpler word like 'Hope' or a direct reference.")

# --- Footer ---
st.markdown("---")
st.caption("Powered by OurManna and Bible-API (Open Source).")