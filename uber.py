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

def main() -> None:
    global mqttc

    # Create mqtt client
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

    # Connect to broker
    mqttc.connect("broker.mqttdashboard.com")

    # Start the MQTT client loop
    mqttc.loop_start()

    # Loopy loop
    while True:

        client.subscribe("iot/topic/1")
        st.write(client.on_message)
        

        # Wait for some time before publishing again, don't spam
        time.sleep(1)

    # Stop the MQTT client
    mqttc.loop_stop()


if __name__== "__main__":
    main()

