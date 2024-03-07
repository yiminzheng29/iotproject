#!/usr/bin/env python3
# -- coding: utf-8 --

import paho.mqtt.client as mqtt
import time


# MQTT client object
mqttc = None

# Topic to publish to.
# **CHANGE THIS TO SOMETHING UNIQUE**
TOPIC = "iot/topic/1"
TOPIC_ALERT = "iot/topic/1"
PAYLOAD_LOW_ALERT = "low light"
PAYLOAD_HIGH_ALERT = "bright light"

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
        print(f"Publish | topic: {TOPIC} | payload: {payload}")

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
