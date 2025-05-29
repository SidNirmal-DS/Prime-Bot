import pandas as pd
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_address(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": API_KEY
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

# Load hotel data
df = pd.read_csv("hotels.csv")

# Add lat/lng columns
latitudes = []
longitudes = []

for index, row in df.iterrows():
    full_address = f"{row['Hotel Name']}, {row['Location']}, Mumbai"
    print(f"Geocoding: {full_address}")
    lat, lng = geocode_address(full_address)
    latitudes.append(lat)
    longitudes.append(lng)
    time.sleep(0.1)  # to respect API rate limits

df["Latitude"] = latitudes
df["Longitude"] = longitudes

# Save updated file
df.to_csv("hotels_with_coordinates.csv", index=False)
print("✅ Done! Saved to hotels_with_coordinates.csv")