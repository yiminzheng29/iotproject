import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from IPython.display import display
import paho.mqtt.client as mqtt
import threading


st.title('Yoga 101')

picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)


# MQTT client object
mqttc = None

def on_message(client, userdata, msg):
    print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")


placeholder = st.empty()

for i in range(10):
    placeholder.text(f"Update {i+1}")
    time.sleep(1)  
