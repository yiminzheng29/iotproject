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


def main() -> None:
    global mqttc

    # Create mqtt client
    mqttc = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

    # Connect to broker
    mqttc.connect("broker.mqttdashboard.com")


    mqttc.subscribe("iot/topic/1")
    
    # Start the MQTT client loop
    mqttc.loop_start()

    

    # Loopy loop
    while True:

        
        st.write(mqttc.on_message)
        

        # Wait for some time before publishing again, don't spam
    mqttc.loop_forever()


if __name__== "__main__":
    main()

