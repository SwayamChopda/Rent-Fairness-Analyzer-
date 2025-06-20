# Rent Fairness Analyzer - Streamlit Version

import pandas as pd
import numpy as np
import streamlit as st
from sklearn.ensemble import RandomForestRegressor
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
from bs4 import BeautifulSoup
import requests

# ------------------- Step 1: Load Real Dataset -------------------
@st.cache_data

def load_data():
    try:
        df = pd.read_csv("real_rent_data.csv")
    except:
        df = pd.DataFrame({
            'location': ['Bandra, Mumbai', 'Andheri, Mumbai', 'Borivali, Mumbai', 'Powai, Mumbai'],
            'latitude': [19.060, 19.119, 19.230, 19.119],
            'longitude': [72.830, 72.846, 72.856, 72.905],
            'area_sqft': [700, 850, 900, 750],
            'bhk': [2, 2, 3, 2],
            'amenities_score': [7, 8, 6, 9],
            'rent_price': [60000, 45000, 48000, 52000]
        })
    return df

mock_data = load_data()

# ------------------- Step 2: Train ML Model -------------------
features = mock_data[['area_sqft', 'bhk', 'amenities_score']]
labels = mock_data['rent_price']
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(features, labels)

# ------------------- Step 3: Scrape Listing (Optional Stub) -------------------
def scrape_listing(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Return dummy values
        return {
            'location': 'Andheri, Mumbai',
            'latitude': 19.119,
            'longitude': 72.846,
            'area_sqft': 800,
            'bhk': 2,
            'amenities_score': 8,
            'actual_price': 50000
        }
    except Exception as e:
        st.error(f"Error scraping URL: {e}")
        return None

# ------------------- Streamlit UI -------------------
st.set_page_config(page_title="Rent Fairness Analyzer", layout="centered")
st.title("🏠 Rent Fairness Analyzer")

# Use session state to persist inputs/results
if 'state' not in st.session_state:
    st.session_state.state = {
        'url': '', 'scraped_data': {}, 'analysis_done': False
    }

url = st.text_input("Paste Rental Listing URL (MagicBricks or 99acres)", value=st.session_state.state['url'])

if url and (url != st.session_state.state['url']):
    scraped = scrape_listing(url)
    if scraped:
        st.session_state.state['url'] = url
        st.session_state.state['scraped_data'] = scraped
        st.session_state.state['analysis_done'] = False

if url:
    scraped = st.session_state.state['scraped_data']
    location = scraped['location']
    latitude = scraped['latitude']
    longitude = scraped['longitude']
    area_sqft = scraped['area_sqft']
    bhk = scraped['bhk']
    amenities_score = scraped['amenities_score']
    actual_price = scraped['actual_price']
else:
    location = st.selectbox("Location", mock_data['location'].unique())
    matched = mock_data[mock_data['location'] == location]
    latitude = float(matched['latitude'].values[0]) if not matched.empty else 19.1
    longitude = float(matched['longitude'].values[0]) if not matched.empty else 72.8
    area_sqft = st.slider("Area (sq ft)", 400, 2000, 800, step=50)
    bhk = st.selectbox("BHK", [1, 2, 3, 4])
    amenities_score = st.slider("Amenities Score (1-10)", 1, 10, 8)
    actual_price = st.number_input("Listed Rent Price (Rs.)", min_value=1000, value=50000, step=500)

if st.button("Analyze Rent"):
    input_features = pd.DataFrame([{
        'area_sqft': area_sqft,
        'bhk': bhk,
        'amenities_score': amenities_score
    }])

    predicted_price = model.predict(input_features)[0]
    diff = actual_price - predicted_price

    st.session_state.state['analysis_done'] = True
    st.session_state.state['predicted_price'] = int(predicted_price)
    st.session_state.state['diff'] = int(diff)
    st.session_state.state['latitude'] = latitude
    st.session_state.state['longitude'] = longitude
    st.session_state.state['actual_price'] = actual_price

if st.session_state.state['analysis_done']:
    st.subheader("📊 Result")
    st.write(f"**Predicted Fair Rent:** Rs. {st.session_state.state['predicted_price']}")
    st.write(f"**Listed Rent:** Rs. {st.session_state.state['actual_price']}")

    if abs(st.session_state.state['diff']) < 2000:
        st.success("Verdict: FAIRLY PRICED")
    elif st.session_state.state['diff'] > 0:
        st.error(f"Verdict: OVERPRICED by Rs. {st.session_state.state['diff']}")
    else:
        st.warning(f"Verdict: UNDERPRICED by Rs. {abs(st.session_state.state['diff'])}")

    # Folium Map for Rent Distribution
    st.subheader("🗺️ Interactive Rent Map")
    fmap = folium.Map(location=[st.session_state.state['latitude'], st.session_state.state['longitude']], zoom_start=12)
    marker_cluster = MarkerCluster().add_to(fmap)

    for _, row in mock_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"{row['location']}\nRent: Rs.{row['rent_price']}",
            icon=folium.Icon(color='blue', icon='home')
        ).add_to(marker_cluster)

    st_folium(fmap, width=700, height=450)

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")
