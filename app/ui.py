# app/oceanintel_app.py
import sys
import csv
from datetime import datetime
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from api.stormglass import fetch_surf_data, fetch_tide_data

if "forecast_requested" not in st.session_state:
    st.session_state.forecast_requested = False

SPOTS = {
    "Huntington Beach": {"lat": 33.6595, "lng": -117.9988},
    "Trestles (San Clemente)": {"lat": 33.3847, "lng": -117.5947},
    "Cardiff Reef": {"lat": 33.0213, "lng": -117.2835},
    "Blacks Beach (San Diego)": {"lat": 32.8872, "lng": -117.2533},
    "Rincon (Santa Barbara)": {"lat": 34.3733, "lng": -119.5246},
}
def run_app():
    st.set_page_config(page_title="🌊 OceanIntel", layout="centered")
    st.title("🏄 OceanIntel: Smart Surf Forecast Advisor")

    # Surf spot selection
    spot_name = st.selectbox("Choose your surf spot:", list(SPOTS.keys()))
    coords = SPOTS[spot_name]

    if st.button("Get Forecast"):
            st.session_state.forecast_requested = True
            # Fetch and store data in session_state
            surf_data = fetch_surf_data(coords["lat"], coords["lng"])
            tide_data = fetch_tide_data(coords["lat"], coords["lng"])

            st.session_state.surf_data = surf_data
            st.session_state.tide_data = tide_data


    if st.session_state.forecast_requested:
        surf_data = st.session_state.get("surf_data", {})
        tide_data = st.session_state.get("tide_data", {})

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
            tide_list = tide_data if isinstance(tide_data, list) else []
            for tide in tide_list[:2]:
                tide_type = tide["type"].capitalize()
                tide_time = tide["time"].replace("T", " ").split("+")[0]
                st.write(f"📌 **{tide_type} tide** at ⏰ {tide_time}")

        # Feedback form
        st.subheader("📝 Rate This Session")

        with st.form("rating_form"):
            rating = st.slider("How would you rate the forecasted conditions?", 1, 5, step=1)
            notes = st.text_input("Optional notes:")
            submit = st.form_submit_button("Submit Rating")
            
            if submit:
                from datetime import datetime
                import csv
                import os

                # ✅ Pull surf data from session state
                surf_data = st.session_state.get("surf_data", {})
                if not surf_data:
                    st.error("Surf data not found. Please fetch forecast again.")
                else:
                    timestamp = datetime.utcnow().isoformat()
                    log_path = os.path.join("data", "session_logs.csv")
                    file_exists = os.path.isfile(log_path)

                    try:
                        with open(log_path, "a", newline="") as csvfile:
                            writer = csv.writer(csvfile)
                            if not file_exists:
                                writer.writerow([
                                    "timestamp", "spot", "swell_height_m", "swell_direction_deg",
                                    "wave_height_m", "wind_speed_mps", "wind_direction_deg",
                                    "rating", "notes"
                                ])
                            writer.writerow([
                                timestamp, spot_name,
                                surf_data.get("swell_height_m"),
                                surf_data.get("swell_direction_deg"),
                                surf_data.get("wave_height_m"),
                                surf_data.get("wind_speed_mps"),
                                surf_data.get("wind_direction_deg"),
                                rating, notes
                            ])
                        st.success("✅ Session rating saved successfully!")
                    except Exception as e:
                        st.error(f"Error saving rating: {e}")


        


        

        

def log_session(spot, surf_data, tide_data, rating):
    file_path = os.path.join("data", "session_logs.csv")
    os.makedirs("data", exist_ok=True)  # Create folder if needed

    # Prepare a row with relevant info
    row = {
        "timestamp": datetime.utcnow().isoformat(),
        "spot": spot,
        "rating": rating,
        "swell_height_m": surf_data.get("swell_height_m", ""),
        "swell_direction_deg": surf_data.get("swell_direction_deg", ""),
        "wave_height_m": surf_data.get("wave_height_m", ""),
        "wind_speed_mps": surf_data.get("wind_speed_mps", ""),
        "wind_direction_deg": surf_data.get("wind_direction_deg", ""),
        "tide_next_type": tide_data[0]["type"] if tide_data else "",
        "tide_next_time": tide_data[0]["time"] if tide_data else "",
    }

    # Check if file exists to write header
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
