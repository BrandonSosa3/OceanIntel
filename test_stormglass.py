from api.stormglass import fetch_surf_data, fetch_tide_data

# Example: Huntington Beach, CA
lat = 33.6595
lng = -117.9988

print("🔹 Testing surf data fetch...")
surf_data = fetch_surf_data(lat, lng)

if "error" in surf_data:
    print("❌ Surf data error:", surf_data["error"])
else:
    print("✅ Surf data fetched:")
    for key, value in surf_data.items():
        print(f"{key}: {value}")

print("\n🔹 Testing tide data fetch...")
tide_data = fetch_tide_data(lat, lng)

if "error" in tide_data:
    print("❌ Tide data error:", tide_data["error"])
else:
    print("✅ Tide extremes for next 24h:")
    for t in tide_data:
        print(f"🌊 {t['type'].capitalize()} tide at {t['time']}")





