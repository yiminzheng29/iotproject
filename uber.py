import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# from IPython.display import display
import paho.mqtt.client as mqtt
import time
from threading import Thread
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx
from streamlit.runtime.scriptrunner.script_run_context import (
    SCRIPT_RUN_CONTEXT_ATTR_NAME,
)
import queue
import functools

HEAD_HTML = f""" <svg data-position="head" class="head %s" xmlns="http://www.w3.org/2000/svg" width="56.594" height="95.031"
        viewBox="0 0 56.594 95.031">
        <path
            d="M15.92 68.5l8.8 12.546 3.97 13.984-9.254-7.38-4.622-15.848zm27.1 0l-8.8 12.546-3.976 13.988 9.254-7.38 4.622-15.848zm6.11-27.775l.108-11.775-21.16-14.742L8.123 26.133 8.09 40.19l-3.24.215 1.462 9.732 5.208 1.81 2.36 11.63 9.72 11.018 10.856-.324 9.56-10.37 1.918-11.952 5.207-1.81 1.342-9.517zm-43.085-1.84l-.257-13.82L28.226 11.9l23.618 15.755-.216 10.37 4.976-17.085L42.556 2.376 25.49 0 10.803 3.673.002 24.415z" />
    </svg>"""
LEFT_SHOULDER_HTML = f"""<svg data-position="shoulder" class="shoulder %s" xmlns="http://www.w3.org/2000/svg" width="109.532" height="46.594"
        viewBox="0 0 109.532 46.594">
        <path
            d="m38.244-.004 1.98 9.232-11.653 2.857-7.474-2.637zM17.005 10.536 12.962 8.35.306 22.35.244 27.675c0 0 16.52-17.015 16.764-17.14zm1.285.58C18.3 11.396.528 30.038.528 30.038L-.01 46.595 6.147 36.045 18.017 30.989 26.374 15.6Z" />
    </svg>"""
RIGHT_SHOULDER_HTML = f"""<svg data-position="shoulder " class="right_shoulder %s" xmlns="http://www.w3.org/2000/svg" width="41" height="46.594"
        viewBox="0 0 41 46.594">
        <path
            d="m6.276-.004-1.98 9.232 11.653 2.857 7.474-2.637zm21.238 10.54 4.044-2.187 12.656 14 .07 5.33c0 0-16.524-17.019-16.769-17.144zm-1.285.58c-.008.28 17.762 18.922 17.762 18.922l.537 16.557-6.157-10.55L26.5 30.988 18.148 15.6Z" />
    </svg>"""
SHOULDER_HTML = f"""<svg data-position="shoulder" class="shoulder %s" xmlns="http://www.w3.org/2000/svg" width="109.532" height="46.594"
        viewBox="0 0 109.532 46.594">
        <path
            d="M38.244-.004l1.98 9.232-11.653 2.857-7.474-2.637zm33.032 0l-1.98 9.232 11.653 2.857 7.474-2.637zm21.238 10.54l4.044-2.187 12.656 14 .07 5.33S92.76 10.66 92.515 10.535zm-1.285.58c-.008.28 17.762 18.922 17.762 18.922l.537 16.557-6.157-10.55L91.5 30.988 83.148 15.6zm-74.224-.58L12.962 8.35l-12.656 14-.062 5.325s16.52-17.015 16.764-17.14zm1.285.58C18.3 11.396.528 30.038.528 30.038L-.01 46.595l6.157-10.55 11.87-5.056L26.374 15.6z" />
    </svg>"""
LEFT_ARM_HTML = f"""<svg data-position="arm" class="left_arm %s" xmlns="http://www.w3.org/2000/svg" width="40.09" height="119.25"
        viewBox="0 0 40.09 119.25">
        <path
            d="m21.12 56.5c-.1236.1323-.2678.2438-.427.33l.935 8.224 12.977-13.89 1.2-8.958C30.624 46.6678 25.7199 51.4413 21.12 56.5Zm1.387 12.522-18.07 48.91 5.757 1.333 19.125-39.44 3.518-22.047zm-5.278-18.96 2.638 18.74-17.2 46.023L.01 113.05 6.654 77.532ZM36.034 37.739c.1244-.0977.2613-.1784.407-.24L40.107 10.154 33.07.015l-7.258 10.58-6.16 37.04.566 4.973C25.1249 47.2797 30.4078 42.3102 36.026 37.738ZM22.288 8.832l-3.3 35.276-2.2-26.238z" />
    </svg>"""
RIGHT_ARM_HTML = f"""<svg data-position="arm" class="right_arm %s" xmlns="http://www.w3.org/2000/svg" width="40.09" height="119.25"
        viewBox="0 0 40.09 119.25">
        <path
            d="m25.244 56.502c.1233.1322.2671.2437.426.33l-.934 8.222-12.977-13.89-1.2-8.958c5.1796 4.4619 10.0824 9.2354 14.681 14.294zm-1.39 12.52 18.073 48.91-5.758 1.333-19.132-39.44-3.52-22.05zm5.28-18.96-2.64 18.74 17.2 46.023 2.658-1.775-6.643-35.518zm-18.8-12.323c-.1247-.0973-.2615-.178-.407-.24l-3.666-27.345 7.039-10.139 7.258 10.58 6.16 37.04-.566 4.973C21.2406 47.2792 15.953 42.3097 10.33 37.738ZM24.078 8.832l3.3 35.276 2.2-26.238z" />
    </svg>"""
ARM_HTML = f"""<svg data-position="arm" class="arm %s" xmlns="http://www.w3.org/2000/svg" width="156.344" height="119.25"
        viewBox="0 0 156.344 119.25">
        <path
            d="M21.12 56.5a1.678 1.678 0 0 1-.427.33l.935 8.224 12.977-13.89 1.2-8.958A168.2 168.2 0 0 0 21.12 56.5zm1.387 12.522l-18.07 48.91 5.757 1.333 19.125-39.44 3.518-22.047zm-5.278-18.96l2.638 18.74-17.2 46.023L.01 113.05l6.644-35.518zm118.015 6.44a1.678 1.678 0 0 0 .426.33l-.934 8.222-12.977-13.89-1.2-8.958A168.2 168.2 0 0 1 135.24 56.5zm-1.39 12.52l18.073 48.91-5.758 1.333-19.132-39.44-3.52-22.05zm5.28-18.96l-2.64 18.74 17.2 46.023 2.658-1.775-6.643-35.518zm-103.1-12.323a1.78 1.78 0 0 1 .407-.24l3.666-27.345L33.07.015l-7.258 10.58-6.16 37.04.566 4.973a151.447 151.447 0 0 1 15.808-14.87zm84.3 0a1.824 1.824 0 0 0-.407-.24l-3.666-27.345L123.3.015l7.258 10.58 6.16 37.04-.566 4.973a151.447 151.447 0 0 0-15.822-14.87zM22.288 8.832l-3.3 35.276-2.2-26.238zm111.79 0l3.3 35.276 2.2-26.238z" />
    </svg>"""
CHEST_HTML = f""" <svg data-position="cheast" class="cheast %s" xmlns="http://www.w3.org/2000/svg" width="86.594" height="45.063"
        viewBox="0 0 86.594 45.063">
        <path
            d="M19.32 0l-9.225 16.488-10.1 5.056 6.15 4.836 4.832 14.07 11.2 4.616 17.85-8.828-4.452-34.7zm47.934 0l9.225 16.488 10.1 5.056-6.15 4.836-4.833 14.07-11.2 4.616-17.844-8.828 4.45-34.7z" />
    </svg>"""
STOMACH_HTML = f"""<svg data-position="stomach" class="stomach %s" xmlns="http://www.w3.org/2000/svg" width="75.25" height="107.594"
        viewBox="0 0 75.25 107.594">
        <path
            d="M19.25 7.49l16.6-7.5-.5 12.16-14.943 7.662zm-10.322 8.9l6.9 3.848-.8-9.116zm5.617-8.732L1.32 2.15 6.3 15.6zm-8.17 9.267l9.015 5.514 1.54 11.028-8.795-5.735zm15.53 5.89l.332 8.662 12.286-2.665.664-11.826zm14.61 84.783L33.28 76.062l-.08-20.53-11.654-5.736-1.32 37.5zM22.735 35.64L22.57 46.3l11.787 3.166.166-16.657zm-14.16-5.255L16.49 35.9l1.1 11.25-8.8-7.06zm8.79 22.74l-9.673-7.28-.84 9.78L-.006 68.29l10.564 14.594 5.5.883 1.98-20.735zM56 7.488l-16.6-7.5.5 12.16 14.942 7.66zm10.32 8.9l-6.9 3.847.8-9.116zm-5.617-8.733L73.93 2.148l-4.98 13.447zm8.17 9.267l-9.015 5.514-1.54 11.03 8.8-5.736zm-15.53 5.89l-.332 8.662-12.285-2.665-.664-11.827zm-14.61 84.783l3.234-31.536.082-20.532 11.65-5.735 1.32 37.5zm13.78-71.957l.166 10.66-11.786 3.168-.166-16.657zm14.16-5.256l-7.915 5.514-1.1 11.25 8.794-7.06zm-8.79 22.743l9.673-7.28.84 9.78 6.862 12.66-10.564 14.597-5.5.883-1.975-20.74z" />
    </svg>"""
LEGS_HTML = f"""<svg data-position="legs" class="legs %s" xmlns="http://www.w3.org/2000/svg" width="93.626" height="286.625"
        viewBox="0 0 93.626 286.625">
        <path
            d="M17.143 138.643l-.664 5.99 4.647 5.77 1.55 9.1 3.1 1.33 2.655-13.755 1.77-4.88-1.55-3.107zm20.582.444l-3.32 9.318-7.082 13.755 1.77 12.647 5.09-14.2 4.205-7.982zm-26.557-12.645l5.09 27.29-3.32-1.777-2.656 8.875zm22.795 42.374l-1.55 4.88-3.32 20.634-.442 27.51 4.65 26.847-.223-34.39 4.87-13.754.663-15.087zM23.34 181.24l1.106 41.267 8.853 33.28-9.628-4.55-16.045-57.8 5.533-36.384zm15.934 80.536l-.664 18.415-1.55 6.435h-4.647l-1.327-4.437-1.55-.222.332 4.437-5.864-1.778-1.55-.887-6.64-1.442-.22-5.214 6.418-10.87 4.426-5.548 10.844-4.437zM13.63 3.076v22.476l15.71 31.073 9.923 30.85L38.23 66.1zm25.49 30.248l.118-.148-.793-2.024L21.9 12.992l-1.242-.44L31.642 40.93zM32.865 44.09l6.812 17.6 2.274-21.596-1.344-3.43zM6.395 61.91l.827 25.34 12.816 35.257-3.928 10.136L3.5 88.133zM30.96 74.69l.345.826 6.47 15.48-4.177 38.342-6.594-3.526 5.715-35.7zm45.5 63.953l.663 5.99-4.647 5.77-1.55 9.1-3.1 1.33-2.655-13.755-1.77-4.88 1.55-3.107zm-20.582.444l3.32 9.318 7.08 13.755-1.77 12.647-5.09-14.2-4.2-7.987zm3.762 29.73l1.55 4.88 3.32 20.633.442 27.51-4.648 26.847.22-34.39-4.867-13.754-.67-15.087zm10.623 12.424l-1.107 41.267-8.852 33.28 9.627-4.55 16.046-57.8-5.533-36.384zM54.33 261.777l.663 18.415 1.546 6.435h4.648l1.328-4.437 1.55-.222-.333 4.437 5.863-1.778 1.55-.887 6.638-1.442.222-5.214-6.418-10.868-4.426-5.547-10.844-4.437zm25.643-258.7v22.476L64.26 56.625l-9.923 30.85L55.37 66.1zM54.48 33.326l-.118-.15.793-2.023L71.7 12.993l1.24-.44L61.96 40.93zm6.255 10.764l-6.812 17.6-2.274-21.595 1.344-3.43zm26.47 17.82l-.827 25.342-12.816 35.256 3.927 10.136 12.61-44.51zM62.64 74.693l-.346.825-6.47 15.48 4.178 38.342 6.594-3.527-5.715-35.7zm19.792 51.75l-5.09 27.29 3.32-1.776 2.655 8.875zM9.495-.007l.827 21.373-7.028 42.308-3.306-34.155zm2.068 27.323L26.24 59.707l3.307 26-6.2 36.58L9.91 85.046l-.827-38.342zM84.103-.01l-.826 21.375 7.03 42.308 3.306-34.155zm-2.066 27.325L67.36 59.707l-3.308 26 6.2 36.58 13.436-37.24.827-38.34z" />
    </svg>"""
LEFT_HANDS_HTML = f"""<svg data-position="hands" class="left_hands %s" xmlns="http://www.w3.org/2000/svg" width="105" height="38.938"
        viewBox="0 0 105 38.938">
        <path
            d="m21.255-.002 2.88 6.9 8.412 1.335.664 12.458-4.427 17.8-2.878-.22 2.8-11.847-2.99-.084-4.676 12.6-3.544-.446 4.4-12.736-3.072-.584-5.978 13.543-4.428-.445 6.088-14.1-2.1-1.25L4.878 34.934 1.114 34.489 12.4 12.9 11.293 11.12.665 15.57 0 13.124 8.635 5.338Z" />
    </svg>"""
RIGHT_HANDS_HTML = f"""<svg data-position="hands" class="right_hands %s" xmlns="http://www.w3.org/2000/svg" width="105" height="38.938"
        viewBox="0 0 105 38.938">
        <path
            d="m33.745-.002-2.88 6.9-8.412 1.335-.664 12.458 4.427 17.8 2.878-.22-2.8-11.847 2.99-.084 4.676 12.6 3.544-.446-4.4-12.736 3.072-.584 5.978 13.543 4.428-.445-6.088-14.1 2.1-1.25 7.528 12.012 3.764-.445L42.6 12.9l1.107-1.78 10.628 4.45.665-2.447-8.635-7.786z" />
    </svg>"""
HANDS_HTML = f"""<svg data-position="hands" class="hands %s" xmlns="http://www.w3.org/2000/svg" width="35" height="38.938"
        viewBox="0 0 35 38.938">
        <path
            d="M21.255-.002l2.88 6.9 8.412 1.335.664 12.458-4.427 17.8-2.878-.22 2.8-11.847-2.99-.084-4.676 12.6-3.544-.446 4.4-12.736-3.072-.584-5.978 13.543-4.428-.445 6.088-14.1-2.1-1.25-7.528 12.012-3.764-.445L12.4 12.9l-1.107-1.78L.665 15.57 0 13.124l8.635-7.786zm162.49 0l-2.88 6.9-8.412 1.335-.664 12.458 4.427 17.8 2.878-.22-2.8-11.847 2.99-.084 4.676 12.6 3.544-.446-4.4-12.736 3.072-.584 5.978 13.543 4.428-.445-6.088-14.1 2.1-1.25 7.528 12.012 3.764-.445L192.6 12.9l1.107-1.78 10.628 4.45.665-2.447-8.635-7.786z" />
    </svg>"""
BODY_HTML = f"""
    <div class="human-body">
    </div>
"""

MQ_HOST = "broker.mqttdashboard.com"
MQ_TOPIC = "iot/topic/yoga1"
q = queue.Queue()
st.title("Yoga Buddy")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    st.toast(f"Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot/topic/yoga1")


body_image = st.empty()


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global q
    q.put(str(msg.payload.decode("utf-8")))


def parsing_to_frontend():
    global body_html_builder, q
    global left_msg, right_msg
    

    if q.empty():
        return body_html_builder
    message = q.get()

    # Transform the signature
    if message == "Hello MQTT!":
        body_part = ''
        pose = None
        orient = ''
        status = ''
    elif ":" in message:
        body_part, status = message.split(":")
        if status[-8:] =='DETECTED': status = 'DETECTED'
        pose = None
        orient = "left" if "left" in body_part.lower() else "right"
    else:
        body_part = (
            message.split("ARRIVED")[0]
            if "ARRIVED" in message
            else message.split("DETECTED")[0]
        )
        pose = message.split(".")[-2].replace("COMPLETE", "").strip()
        orient = None
        status = "COMPLETE"
    # factory to get class html
    
    if status == 'DETECTED':
        class_html = 'complete'
    else:
        class_html = status.lower().replace("too", "").strip()
    # factory to return body_part html to light up according the status
    body_part = body_part.lower()
    st.toast(f"SIGNAL: {body_part=}, {pose=}, {status=}, {orient=}")
    # left_msg, right_msg = "", ""



    if orient == "left":
        left_msg = message
        if "hand" in body_part:
            left_hands_html = LEFT_HANDS_HTML % class_html
            right_hands_html = RIGHT_HANDS_HTML % ""
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_arm_html = LEFT_ARM_HTML % class_html
            right_arm_html = RIGHT_ARM_HTML % ""
        if "shoulder" in body_part:
            left_shoulder_html = LEFT_SHOULDER_HTML % class_html
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
            left_arm_html = LEFT_ARM_HTML % ""
            right_arm_html = RIGHT_ARM_HTML % ""
        if "arm" in body_part:
            left_arm_html = LEFT_ARM_HTML % class_html
            right_arm_html = RIGHT_ARM_HTML % ""
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
    elif orient == "right":
        right_msg = message
        if "hand" in body_part:
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % class_html
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_arm_html = LEFT_ARM_HTML % ""
            right_arm_html = RIGHT_ARM_HTML % class_html
        if "shoulder" in body_part:
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % class_html
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
            left_arm_html = LEFT_ARM_HTML % ""
            right_arm_html = RIGHT_ARM_HTML % ""
        if "arm" in body_part:
            left_arm_html = LEFT_ARM_HTML % ""
            right_arm_html = RIGHT_ARM_HTML % class_html
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
    elif status == "COMPLETE":
        print(message)
        if pose == "POSE 1": 
            left_msg = "Mountain Pose achieved.\nInhale deeply and extend your body upwards before moving to a Forward Fold."
            right_msg = ""
        if pose == "POSE 2": 
            left_msg = "Forward Fold achieved.\nFeel the stretch in your hamstrings and start to release tension in the back and neck."
            right_msg = ""

        class_html = "complete"
        if "hand" in body_part:
            left_hands_html = LEFT_HANDS_HTML % class_html
            right_hands_html = RIGHT_HANDS_HTML % class_html
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_arm_html = LEFT_ARM_HTML % class_html
            right_arm_html = RIGHT_ARM_HTML % class_html
        if "shoulder" in body_part:
            left_shoulder_html = LEFT_SHOULDER_HTML % class_html
            right_shoulder_html = RIGHT_SHOULDER_HTML % class_html
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
            left_arm_html = LEFT_ARM_HTML % ""
            right_arm_html = RIGHT_ARM_HTML % ""
        if "arm" in body_part:
            left_arm_html = LEFT_ARM_HTML % class_html
            right_arm_html = RIGHT_ARM_HTML % class_html
            left_shoulder_html = LEFT_SHOULDER_HTML % ""
            right_shoulder_html = RIGHT_SHOULDER_HTML % ""
            left_hands_html = LEFT_HANDS_HTML % ""
            right_hands_html = RIGHT_HANDS_HTML % ""
    else:
        left_hands_html = LEFT_HANDS_HTML % ""
        right_hands_html = RIGHT_HANDS_HTML % ""
        left_shoulder_html = LEFT_SHOULDER_HTML % ""
        right_shoulder_html = RIGHT_SHOULDER_HTML % ""
        left_arm_html = LEFT_ARM_HTML % ""
        right_arm_html = RIGHT_ARM_HTML % ""
    

    # body_html builder skeleton
    body_html_builder = f"""
        <div class="human-body">
            {HEAD_HTML % ''}
            {left_shoulder_html}
            {right_shoulder_html}
            {left_arm_html}
            {right_arm_html}
            {CHEST_HTML % ''}
            {STOMACH_HTML % ''}
            {LEGS_HTML % ''}
            {left_hands_html}
            {right_hands_html}
        </div>
    """
    return body_html_builder, left_msg, right_msg


body_html_builder = f"""
        <div class="human-body">
            {HEAD_HTML % ''}
            {LEFT_SHOULDER_HTML  % ''}
            {RIGHT_SHOULDER_HTML  % ''}
            {LEFT_ARM_HTML % ''}
            {RIGHT_ARM_HTML % ''}
            {CHEST_HTML % ''}
            {STOMACH_HTML % ''}
            {LEGS_HTML % ''}
            {LEFT_HANDS_HTML % ''}
            {RIGHT_HANDS_HTML % ''}
        </div>
    """


def main():
    global body_html_builder
    global left_msg, right_msg

    left_msg, right_msg = "", ""
    
    col1, col2 = st.columns(2)

    with col1:
        col1.caption(left_msg)
        left_prompt = col1.empty()
    with col2:
        col2.caption(right_msg)   
        right_prompt = col1.empty()
            
    # hexcode - classname - color:
    # ff9999 fast - red
    # 334ACD slow - blue
    # 62CE34 complete - green
    # 62CE34 detected - green
    st.write(
        """<style>.human-body {width: 207px;position: relative;padding-top: 240px;height: 260px;display: block;margin: 40px auto;}.human-body svg:hover {cursor: pointer;}.human-body svg:hover path {fill: #ff7d16;}.human-body svg.fast path{fill:#ff9999;}.human-body svg.slow path{fill:#334ACD;}.human-body svg.complete path{fill:#62CE34;}.human-body svg {position: absolute;left: 50%;fill: #57c9d5;}.human-body svg.head {margin-left: -28.5px;top: -6px;}.human-body svg.shoulder {margin-left: -53.5px;top: 69px;}.human-body svg.left_shoulder {margin-left: -53.5px;top: 69px;}.human-body svg.right_shoulder {margin-left: 10px;top: 69px;}.human-body svg.arm {margin-left: -78px;top: 112px;}.human-body svg.left_arm {margin-left: -78px;top: 112px;}.human-body svg.right_arm {margin-left: 34px;top: 112px;}.human-body svg.cheast {margin-left: -43.5px;top: 88px;}.human-body svg.stomach {margin-left: -37.5px;top: 130px;}.human-body svg.legs {margin-left: -46.5px;top: 205px;z-index: 9999;}.human-body svg.hands {margin-left: -102.5px;top: 224px;}.human-body svg.left_hands {margin-left: -102.5px;top: 224px;}.human-body svg.right_hands {margin-left: 49px;top: 224px;}#area {display: block;width: 100%;clear: both;padding: 10px;text-align: center;font-size: 25px;font-family: Courier New;color: #a5a5a5;}#area #data {color: black;}</style>""",
        unsafe_allow_html=True,
    )
    # Placeholder for female body
    body_image = st.empty()
    body_image.write(body_html_builder, unsafe_allow_html=True)
    # Create empty placeholder for message to push into
    # col1 for iot push data
    # col2 for sidebar / plot

    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message

    mqttc.connect(MQ_HOST)
    mqttc.subscribe(MQ_TOPIC)
    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    st.toast(f"Created MQTT {MQ_HOST} with topic {MQ_TOPIC} - SUCCESS", icon="🎉")
    if "status" not in st.session_state:
        thread = Thread(target=mqttc.loop_forever)
        add_script_run_ctx(thread=thread, ctx=get_script_run_ctx())
        thread.start()
        st.session_state["status"] = "created"

    # Looping while True
    # Wait for 0.5s if no new message then loop
    while True:
        if not q.empty():
            body_html_builder, left_msg, right_msg  = parsing_to_frontend()
            left_prompt.write(left_msg)
            right_prompt.write(right_msg)
            body_image.empty()
            body_image.write(body_html_builder, unsafe_allow_html=True)
            print(f"{body_html_builder=}")
        time.sleep(0.1)


if __name__ == "__main__":
    main()
