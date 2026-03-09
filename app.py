import streamlit as st
import requests
import re

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="TCRRA Bible Study Hub", page_icon="📖", layout="wide")

# --- 2. CLEANING UTILITY ---
def clean_html(raw_html):
    """Removes <u> tags and other HTML from the Bible text"""
    if not raw_html:
        return ""
    # This removes everything inside < > brackets (like <u> or </u>)
    clean_text = re.sub('<.*?>', '', raw_html)
    return clean_text

# --- 3. UPDATED API FUNCTIONS ---

def get_daily_verse():
    """Fetches a random verse and cleans the HTML"""
    try:
        url = "https://bolls.life/get-random-verse/KJV/"
        response = requests.get(url, timeout=5).json()
        return {
            "text": clean_html(response['text']),
            "ref": f"{response['book']} {response['chapter']}:{response['verse']}"
        }
    except:
        return {"text": "Trust in the Lord with all thine heart.", "ref": "Proverbs 3:5"}

def search_bible(query, translation):
    """Searches the database using the updated Bolls v2 URL"""
    # The URL requires a space before the 'search' parameter in some versions of the API
    url = f"https://bolls.life/v2/find/{translation}/?search={query}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []
    except Exception as e:
        return None

# --- 4. USER INTERFACE ---

st.title("📖 Bible Study Hub")

# Verse of the Day
votd = get_daily_verse()
st.markdown(f"""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 8px solid #4CAF50;">
        <p style="font-size: 1.2em; font-style: italic;">"{votd['text']}"</p>
        <strong>— {votd['ref']}</strong>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("Search Settings")
    translation_options = {
        "King James Version": "KJV",
        "New King James": "NKJV",
        "English Standard Version": "ESV",
        "Yoruba Bible": "YOR"
    }
    selected_ver = st.selectbox("Translation", list(translation_options.keys()))
    ver_code = translation_options[selected_ver]

# Main Search Area
st.subheader("🔍 Search by Topic")
user_input = st.text_input("Enter a keyword (e.g., 'Healing', 'Peace')", placeholder="Search...")

if user_input:
    with st.spinner(f"Searching in {selected_ver}..."):
        results = search_bible(user_input, ver_code)
        
        if results:
            st.success(f"Found {len(results)} matches.")
            for item in results:
                ref = f"{item['book']} {item['chapter']}:{item['verse']}"
                with st.expander(f"📜 {ref}"):
                    # We clean the text here too
                    st.write(clean_html(item['text']))
        elif results == []:
            st.warning("No verses found for that word. Try 'Faith' or 'Love'.")
        else:
            st.error("There was a connection issue with the database. Please try again in a moment.")

st.caption("Data provided by Bolls Bible API.")