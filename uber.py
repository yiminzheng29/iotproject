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


# Initialize session state
if 'mqtt_data' not in st.session_state:
    st.session_state['mqtt_data'] = "Waiting for data..."

# Callback function for when a connection is established
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("iot/topic/1")

# Callback function for when a message is received
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    # Update Streamlit's session state
    st.session_state['mqtt_data'] = msg.payload.decode()

# Setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
client.connect("mqtt_broker_address", 1883, 60)

# Run the MQTT client on a separate thread to avoid blocking Streamlit's main thread
thread = threading.Thread(target=client.loop_forever)
thread.start()

# Streamlit app main loop
def main():
    st.title("MQTT Data Receiver")
    if st.button("Refresh Data"):
        st.write(st.session_state['mqtt_data'])

main()
