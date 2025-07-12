# api/stormglass.py

import requests
from config import STORMGLASS_API_KEY
from datetime import datetime, timedelta

def fetch_surf_data(lat, lng):
    url = "https://api.stormglass.io/v2/weather/point"
    params = {
        "lat": lat,
        "lng": lng,
        "params": ",".join([
            "swellHeight",
            "swellDirection",
            "waveHeight",
            "windSpeed",
            "windDirection"
        ]),
        "source": "noaa"
    }
    headers = {
        "Authorization": STORMGLASS_API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch surf data: {response.status_code}"}

    data = response.json()

    try:
        first_hour = data["hours"][0]
        clean_data = {
            "swell_height_m": first_hour["swellHeight"]["noaa"],
            "swell_direction_deg": first_hour["swellDirection"]["noaa"],
            "wave_height_m": first_hour["waveHeight"]["noaa"],
            "wind_speed_mps": first_hour["windSpeed"]["noaa"],
            "wind_direction_deg": first_hour["windDirection"]["noaa"],
        }
        return clean_data
    except Exception as e:
        return {"error": f"Unexpected surf data structure: {e}"}


def fetch_tide_data(lat, lng):
    """Fetch tide extremes (high/low tides) for today"""
    url = "https://api.stormglass.io/v2/tide/extremes/point"
    now = datetime.utcnow()
    end = now + timedelta(days=1)

    params = {
        "lat": lat,
        "lng": lng,
        "start": now.isoformat(),
        "end": end.isoformat(),
    }
    headers = {
        "Authorization": STORMGLASS_API_KEY
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch tide data: {response.status_code}"}

    try:
        tide_data = response.json()["data"]
        return tide_data  # List of dicts with "time" and "type" (high/low)
    except Exception as e:
        return {"error": f"Unexpected tide data structure: {e}"}



    



