import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Windborne Balloon Tracker", layout="wide")
st.title("🎈 Live Windborne Balloon Tracker")

# --- IMPROVED DATA FETCHING ---
@st.cache_data(ttl=300)
def get_balloon_data():
    base_url = "https://a.windbornesystems.com/treasure/{:02d}.json"
    
    # Try the last 12 hours one by one until we find valid data
    for i in range(12):
        try:
            url = base_url.format(i)
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                # Check if it looks like a valid list of coordinates
                if isinstance(data, list) and len(data) > 0:
                    st.toast(f"✅ Loaded data from {i} hour(s) ago")
                    
                    # Clean the data
                    clean_data = []
                    for entry in data:
                        if isinstance(entry, list) and len(entry) >= 2:
                            clean_data.append({
                                "lat": entry[0],
                                "lon": entry[1],
                                "altitude": entry[2] if len(entry) > 2 else 0
                            })
                    return pd.DataFrame(clean_data)
        except:
            continue
            
    return pd.DataFrame()

# --- DISPLAY LOGIC ---
df_balloons = get_balloon_data()

if not df_balloons.empty:
    st.metric("Active Balloons Tracked", len(df_balloons))
    st.map(df_balloons, color="#0000FF", size=20)
    st.caption("Map shows valid balloon positions retrieved from Windborne systems.")
else:
    st.error("⚠️ Could not retrieve any data from the last 12 hours. The API might be down.")

st.markdown("---")
st.markdown("**Notes:** This app robustly scans the last 12 hours of telemetry to handle potential feed corruption.")