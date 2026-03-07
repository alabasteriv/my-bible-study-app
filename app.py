import streamlit as st
import requests
import random

# --- 1. APP CONFIGURATION ---
st.set_page_config(
    page_title="Bible Topic Study",
    page_icon="📖",
    layout="centered"
)

# --- 2. CUSTOM STYLING (Optional but nice) ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; }
    .verse-box { 
        padding: 20px; 
        border-radius: 10px; 
        background-color: white; 
        border-left: 5px solid #4A90E2;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. VERSE OF THE DAY LOGIC ---
# A curated list of daily inspirations for your community
daily_options = [
    {"ref": "Isaiah 40:31", "text": "But they that wait upon the Lord shall renew their strength..."},
    {"ref": "Philippians 4:13", "text": "I can do all things through Christ which strengtheneth me."},
    {"ref": "Psalm 23:1", "text": "The Lord is my shepherd; I shall not want."},
    {"ref": "John 14:27", "text": "Peace I leave with you, my peace I give unto you..."},
    {"ref": "Proverbs 3:5", "text": "Trust in the Lord with all thine heart; and lean not unto thine own understanding."}
]

# --- 4. API CONNECTION FUNCTION ---
def fetch_scripture(query):
    """Links to the web-based Bible database API"""
    url = f"https://bible-api.com/{query}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return "Connection Error"

# --- 5. APP UI LAYOUT ---
st.title("📖 Bible Study Helper")
st.write("Find strength and wisdom in the Word.")

# Display Verse of the Day
st.subheader("🌟 Verse of the Day")
votd = random.choice(daily_options)
st.markdown(f"""
<div class="verse-box">
    <i>"{votd['text']}"</i><br>
    <strong>— {votd['ref']}</strong>
</div>
""", unsafe_allow_html=True)

st.divider()

# Search Section
st.subheader("🔍 Search by Topic or Reference")
search_query = st.text_input("Example: 'Peace', 'Hope', or 'John 3:16'", placeholder="Type here...")

if search_query:
    with st.spinner('Searching the scriptures...'):
        data = fetch_scripture(search_query)
        
        if data and isinstance(data, dict):
            st.success(f"Results for: {data.get('reference')}")
            
            # Display result in a clean format
            st.markdown(f"### {data.get('reference')}")
            st.write(data.get('text'))
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy Verse"):
                    st.write("Text ready to copy!") 
            with col2:
                st.info("💡 Use this text for your sermon slides.")
                
        else:
            st.error("We couldn't find that specific topic. Try a direct verse like 'Psalm 23' or a common word like 'Faith'.")

# Footer
st.markdown("---")
st.caption("Built for Gospel Ministry and Bible Study. Powered by Bible-API.")