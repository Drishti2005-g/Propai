# utils/map_utils.py

import folium
from folium.plugins import MarkerCluster

# Default fallback coordinates (Bangalore center)
DEFAULT_LAT = 12.9716
DEFAULT_LON = 77.5946


def create_map(df):
    """
    Create a folium map with:
    - purple markers
    - clustering
    - popup details
    - auto zoom
    """

    # base map
    m = folium.Map(location=[DEFAULT_LAT, DEFAULT_LON], zoom_start=11, tiles="cartodbpositron")

    # marker cluster
    cluster = MarkerCluster().add_to(m)

    for _, row in df.iterrows():

        lat = row.get("lat", DEFAULT_LAT)
        lon = row.get("lon", DEFAULT_LON)

        title = row.get("title", "No Title")
        location = row.get("location", "Unknown")
        price = row.get("price", "N/A")

        popup_html = f"""
        <div style="font-family: sans-serif;">
            <h4 style="margin:0;padding:0;">{title}</h4>
            <p style="margin:2px 0;">📍 {location}</p>
            <p style="margin:2px 0;">💰 ₹ {price}</p>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=popup_html,
            tooltip=title,
            icon=folium.Icon(color="purple", icon="home", prefix="fa")
        ).add_to(cluster)

    return m



def map_to_streamlit(m):
    """Safely render Folium map inside Streamlit."""
    from streamlit_folium import st_folium
    return st_folium(m, width=900, height=500)