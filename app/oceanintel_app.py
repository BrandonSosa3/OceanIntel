# app/oceanintel_app.py
import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from api.stormglass import fetch_surf_data, fetch_tide_data

SPOTS = {
    "Huntington Beach": {"lat": 33.6595, "lng": -117.9988},
    "Trestles (San Clemente)": {"lat": 33.3847, "lng": -117.5947},
    "Cardiff Reef": {"lat": 33.0213, "lng": -117.2835},
    "Blacks Beach (San Diego)": {"lat": 32.8872, "lng": -117.2533},
    "Rincon (Santa Barbara)": {"lat": 34.3733, "lng": -119.5246},
}

st.set_page_config(page_title="🌊 OceanIntel", layout="centered")
st.title("🏄 OceanIntel: Smart Surf Forecast Advisor")

# Surf spot selection
spot_name = st.selectbox("Choose your surf spot:", list(SPOTS.keys()))
coords = SPOTS[spot_name]

if st.button("Get Forecast"):
    with st.spinner("Fetching surf and tide data..."):
        surf_data = fetch_surf_data(coords["lat"], coords["lng"])
        tide_data = fetch_tide_data(coords["lat"], coords["lng"])

    if "error" in surf_data:
        st.error(surf_data["error"])
    else:
        st.subheader("🌊 Surf Conditions (Now)")
        st.metric("Swell Height", f"{surf_data['swell_height_m']} m")
        st.metric("Swell Direction", f"{surf_data['swell_direction_deg']}°")
        st.metric("Wave Height", f"{surf_data['wave_height_m']} m")
        st.metric("Wind Speed", f"{surf_data['wind_speed_mps']} m/s")
        st.metric("Wind Direction", f"{surf_data['wind_direction_deg']}°")

    if "error" in tide_data:
        st.warning("⚠️ Tide data not available.")
    else:
        st.subheader("🌊 Tide Extremes (Next 24h)")
        for tide in tide_data[:2]:  # Show next 2 tides
            tide_type = tide["type"].capitalize()
            tide_time = tide["time"].replace("T", " ").split("+")[0]
            st.write(f"📌 **{tide_type} tide** at ⏰ {tide_time}")
