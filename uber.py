import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from IPython.display import display
import paho.mqtt.client as mqtt
import time
import threading


st.title('Yoga 101')

picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)


# Callback when connecting to the MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribe to the desired topic
    client.subscribe("iot/topic/1")

# Callback when receiving a message from the MQTT broker
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    st.write(message)
    print(f"Received message: {message} on topic {msg.topic}")
    # Update Streamlit's session state
    st.session_state['latest_message'] = message

# Initialize MQTT client and configure callbacks
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker (adjust hostname and port as necessary)
client.connect("broker.mqttdashboard.com", 1883, 60)

# Start MQTT client in a background thread
thread = threading.Thread(target=client.loop_forever)
thread.start()

# Streamlit app
def main():
    # Initialize session state for storing the latest message
    if 'latest_message' not in st.session_state:
        st.session_state['latest_message'] = "No message yet."

    # Display the latest message
    st.title("MQTT Messages")
    st.write(f"Latest message: {st.session_state['latest_message']}")

    # You could also add a button to clear the message or perform other actions

if __name__ == "__main__":
    main()


