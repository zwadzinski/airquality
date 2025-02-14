import requests
import streamlit as st
from functions import interpret_air_quality, display_particle_counts

# Replace with the appropriate public URL from ngrok or your endpoint
api_url = "https://whale-pro-marmot.ngrok-free.app/data"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    sensor_data = response.json()
    st.header("Air Quality Reading")
    st.write(interpret_air_quality(sensor_data))
    st.subheader("Other Measurements")
    st.text(display_particle_counts(sensor_data))
except Exception as e:
    st.error(f"Error fetching data: {e}")

if st.button("Refresh"):
    st.experimental_rerun()