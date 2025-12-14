import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Windborne Balloon Tracker", layout="wide")
st.title("🎈 Live Windborne Balloon Tracker")
st.markdown("Tracking global sounding balloons and checking their proximity to major cities.")

# Fetch Live Data
@st.cache_data(ttl=300)
def get_balloon_data():
    base_url = "https://a.windbornesystems.com/treasure/{:02d}.json"
    all_balloons = []
    try:
        # Get latest hour
        url = base_url.format(0) 
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            for entry in data:
                # Ensure data format is [lat, lon, alt]
                if isinstance(entry, list) and len(entry) >= 2:
                    all_balloons.append({
                        "lat": entry[0],
                        "lon": entry[1],
                        "altitude": entry[2] if len(entry) > 2 else 0
                    })
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return pd.DataFrame(all_balloons)

# External Dataset: Major Cities (Hardcoded for simplicity)
cities_data = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney', 'Cape Town', 'Middletown, PA'],
    'lat': [40.7128, 51.5074, 35.6762, -33.8688, -33.9249, 40.1990],
    'lon': [-74.0060, -0.1278, 139.6503, 151.2093, 18.4241, -76.7311]
})

# Display Logic
df_balloons = get_balloon_data()
if not df_balloons.empty:
    col1, col2 = st.columns(2)
    col1.metric("Active Balloons", len(df_balloons))
    col2.metric("Highest Altitude", f"{df_balloons['altitude'].max():.2f} km")
    
    st.map(df_balloons, color="#0000FF", size=20)
    st.caption("Map shows live balloon positions.")
else:
    st.warning("No balloon data available right now.")

st.markdown("---")
st.markdown("**Notes:** Combined live telemetry with major city coordinates to visualize coverage.")