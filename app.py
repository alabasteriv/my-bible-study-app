import streamlit as st
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="TCRRA Bible Study Hub",
    page_icon="📖",
    layout="wide"
)

# --- 2. API FUNCTIONS (Using Bolls Bible API - No Key Needed) ---

def get_daily_verse():
    """Fetches a random verse for the 'Daily' section"""
    try:
        # Bolls has a random verse endpoint
        url = "https://bolls.life/get-random-verse/KJV/"
        response = requests.get(url, timeout=5).json()
        return {
            "text": response['text'],
            "ref": f"{response['book']} {response['chapter']}:{response['verse']}"
        }
    except:
        return {"text": "For I know the plans I have for you, declares the Lord.", "ref": "Jeremiah 29:11"}

def search_bible(query, translation):
    """Searches for verses by topic or keyword"""
    # Bolls search endpoint: /v2/find/<translation>/?search=<query>
    url = f"https://bolls.life/v2/find/{translation}/"
    params = {"search": query, "limit": 10} # We limit to 10 for speed
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            return response.json().get('results', [])
        return None
    except:
        return None

# --- 3. USER INTERFACE ---

st.title("📖 Bible Study Hub")
st.write("A free tool for search and study—no account or keys required.")

# Verse of the Day Section
votd = get_daily_verse()
st.markdown(f"""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 8px solid #4CAF50;">
        <h4 style="margin-top:0; color:#4CAF50;">✨ Random Inspiration</h4>
        <p style="font-size: 1.1em; font-style: italic;">"{votd['text']}"</p>
        <strong>— {votd['ref']}</strong>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Search Sidebar
with st.sidebar:
    st.header("Search Settings")
    # Mapping common names to Bolls API codes
    translation_options = {
        "King James Version": "KJV",
        "New King James": "NKJV",
        "English Standard Version": "ESV",
        "Yoruba Bible": "YOR"
    }
    selected_ver = st.selectbox("Translation", list(translation_options.keys()))
    ver_code = translation_options[selected_ver]
    
    st.caption("Searching in: " + selected_ver)

# Main Search Area
st.subheader("🔍 Search by Topic")
user_input = st.text_input("Enter a keyword (e.g., 'Love', 'Strength', 'Patience')", placeholder="Type here...")

if user_input:
    with st.spinner(f"Searching the Word in {selected_ver}..."):
        results = search_bible(user_input, ver_code)
        
        if results:
            st.success(f"Found {len(results)} verses for '{user_input}'")
            for item in results:
                # Bolls results include the verse text and reference parts
                ref = f"{item['book']} {item['chapter']}:{item['verse']}"
                with st.expander(f"📜 {ref}"):
                    st.write(item['text'])
                    if st.button(f"Copy {ref}", key=item['pk']):
                        st.info("Verse text ready to highlight and copy!")
        else:
            st.warning("No verses found for that topic. Try a simpler keyword.")

# Footer
st.markdown("---")
st.caption("Data provided by the Open Source Bolls Bible API.")