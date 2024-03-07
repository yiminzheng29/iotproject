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

        # Data that will be published
        payload="light:200"

        # Print some debugging info
        st.write(payload)

        # Publish data to MQTT broker
        mqttc.publish(topic=TOPIC, payload=payload, qos=0)
        
        # throw alert if value below 100
        val = int(payload.split(":")[-1])
        if val<100:
            mqttc.publish(topic=TOPIC_ALERT, payload=PAYLOAD_LOW_ALERT, qos=0)

        # throw alert if value above 500
        elif val>500:
            mqttc.publish(topic=TOPIC_ALERT, payload=PAYLOAD_HIGH_ALERT, qos=0)
            
        # Wait for some time before publishing again, don't spam
        time.sleep(5)

    # Stop the MQTT client
    mqttc.loop_stop()


if __name__== "__main__":
    main()

