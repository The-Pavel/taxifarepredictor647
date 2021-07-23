import streamlit as st
import pandas as pd
from datetime import datetime, time
# import pydeck as pdk
import requests

pu_lat = False
pu_lon = False
do_lat = False
do_lon = False
# title
st.title('NYC Taxi Fare Estimator')
# st.map()
# date
pu_date = st.sidebar.date_input(label = 'Pickup Date?')
# time
pu_time = st.sidebar.time_input(label = 'Pickup Time')
# pickup
pu = st.sidebar.text_input(label = 'Pickup Location')
if pu:
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={pu}&format=json").json()[0]
    pu_lat = response['lat']
    pu_lon = response['lon']
    # map
    # st.map(pd.DataFrame({'lat': [pu_lat], 'lon': [pu_lon]}))
# dropoff
do = st.sidebar.text_input(label = 'Dropoff Location')
if do and pu:
    response = requests.get(f"https://nominatim.openstreetmap.org/search?q={do}&format=json").json()[0]
    do_lat = response['lat']
    do_lon = response['lon']
    st.map(pd.DataFrame({'lat': [float(pu_lat), float(do_lat)], 'lon': [float(pu_lon), float(do_lon)]}))
# passenger count
pas_count = st.sidebar.number_input(label = 'Number of Passengers', min_value = 0, max_value = 8, key = 'p_count')
st.write()
# prediction
pu_input = pu_lat and pu_lon
do_input = do_lat and do_lon
if pas_count and pu_date and pu_time and pu_input and do_input:
    params = {
    "pickup_datetime": f"{pu_date}" + ' ' + f"{pu_time}",
    "pickup_longitude": pu_lon,
    "pickup_latitude": pu_lat,
    "dropoff_longitude": do_lon,
    "dropoff_latitude": do_lat,
    "passenger_count": pas_count
    }
    pred_response = requests.get(f"https://taxifare.lewagon.ai/predict", params)
    st.write(pred_response.json()['prediction'])
