import pandas as pd
import folium
from geopy.distance import geodesic

# Load the dataset
df = pd.read_csv("hotels_with_coordinates.csv")

# Reference location: Chhatrapati Shivaji Maharaj International Airport, Mumbai
airport_coords = (19.0896, 72.8656)

# Filter hotels within 3 km radius of the airport
def is_within_radius(row, center=airport_coords, radius_km=3):
    hotel_coords = (row['Latitude'], row['Longitude'])
    return geodesic(center, hotel_coords).km <= radius_km

nearby_df = df[df.apply(is_within_radius, axis=1)]

# Create map centered on airport
mumbai_map = folium.Map(location=airport_coords, zoom_start=13)

# Add markers for nearby hotels
for _, row in nearby_df.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=f"{row['Hotel Name']} ({row['Final Price']} INR)",
        tooltip=row['Hotel Name'],
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(mumbai_map)

# Save to HTML
mumbai_map.save("nearby_hotels_map.html")
print("✅ Map saved as 'nearby_hotels_map.html'")