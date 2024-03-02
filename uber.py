import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from IPython.display import display


st.title('Yoga 101')



def init_real_time_plot():
    global fig_x, fig_y, fig_z
    # Initialize figures with two traces each: actual values and moving averages
    fig_x = go.FigureWidget(data=[
        go.Scatter(x=[], y=[], mode='lines+markers', name='X Values'),
        go.Scatter(x=[], y=[], mode='lines', name='X Moving Avg', line=dict(color='red'))])
    fig_y = go.FigureWidget(data=[
        go.Scatter(x=[], y=[], mode='lines+markers', name='Y Values'),
        go.Scatter(x=[], y=[], mode='lines', name='Y Moving Avg', line=dict(color='red'))])
    fig_z = go.FigureWidget(data=[
        go.Scatter(x=[], y=[], mode='lines+markers', name='Z Values'),
        go.Scatter(x=[], y=[], mode='lines', name='Z Moving Avg', line=dict(color='red'))])

    # Set titles and display the figures
    fig_x.update_layout(title_text='Real-Time X Values')
    fig_y.update_layout(title_text='Real-Time Y Values')
    fig_z.update_layout(title_text='Real-Time Z Values')

    st.plotly_chart(fig_x, theme=None, use_container_width=True)
   # display(fig_x, fig_y, fig_z)

def send_alert_to_microbit(serial_connection, message):
    """
    Sends an alert message to the microbit via the serial connection.

    Args:
    - serial_connection: The open serial connection to the microbit.
    - message: The message to send as a string.
    """
    serial_connection.write(message.encode())
    # serial_connection.close()

import serial
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def read_serial_data(port, baud_rate=115200, timeout=1, duration=10):
    
    global ser
    init_real_time_plot()  # Ensure you have initialized a Plotly FigureWidget globally
    ser = serial.Serial(port, baud_rate, timeout=timeout)
    end_time = time.time() + duration
    value_index = 0  # Cycle through 0 (x), 1 (y), 2 (z)
    sample_index = 0  # Increment for each new set of x, y, z values

    
    try:
        while True: # if want to read data continuously
        # while time.time() < end_time:  # Continuously read and plot data
            if ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                if data:
                    try:
                        value = int(data)
                        # Determine which plot to update based on value_index
                        if value_index == 0:  # X value
                            add_data_to_plot(ser, value, None, None, sample_index)
                        elif value_index == 1:  # Y value
                            add_data_to_plot(ser, None, value, None, sample_index)
                        elif value_index == 2:  # Z value
                            add_data_to_plot(ser, None, None, value, sample_index)
                            sample_index += 1  # Increment sample_index after a full cycle
                        
                        value_index = (value_index + 1) % 3  # Cycle through 0, 1, 2
                    except ValueError:
                        pass  # Ignore non-integer values
                time.sleep(0.1)  # Adjust based on your data rate
    finally:
        ser.close()


# Define window size for the moving average
N = 10  # Example window size
# Initialize rolling windows for x, y, z values
rolling_window_x, rolling_window_y, rolling_window_z = [], [], []

THRESHOLD_X = -150
THRESHOLD_Y = 250
THRESHOLD_Z = 250

def add_data_to_plot(serial_connection, x_new, y_new, z_new, sample_index):
    global rolling_window_x, rolling_window_y, rolling_window_z
    
    # Update and calculate moving average for X values, check threshold
    if x_new is not None:
        rolling_window_x.append(x_new)
        rolling_window_x = rolling_window_x[-N:]
        x_moving_avg = sum(rolling_window_x) / len(rolling_window_x)
        
        with fig_x.batch_update():
            fig_x.data[0].x += (sample_index,)
            fig_x.data[0].y += (x_new,)
            fig_x.data[1].x += (sample_index,)
            fig_x.data[1].y += (x_moving_avg,)
        
        if x_moving_avg > THRESHOLD_X:
            # print('alertx')
            send_alert_to_microbit(serial_connection, "Alert X")

    # Repeat the process for Y and Z values
    if y_new is not None:
        rolling_window_y.append(y_new)
        rolling_window_y = rolling_window_y[-N:]
        y_moving_avg = sum(rolling_window_y) / len(rolling_window_y)
        
        with fig_y.batch_update():
            fig_y.data[0].x += (sample_index,)
            fig_y.data[0].y += (y_new,)
            fig_y.data[1].x += (sample_index,)
            fig_y.data[1].y += (y_moving_avg,)
            
        # if y_moving_avg > THRESHOLD_Y:
        #     # print('alerty')
        #     send_alert_to_microbit(serial_connection, "Alert Y")
            
    if z_new is not None:
        rolling_window_z.append(z_new)
        rolling_window_z = rolling_window_z[-N:]
        z_moving_avg = sum(rolling_window_z) / len(rolling_window_z)
        
        with fig_z.batch_update():
            fig_z.data[0].x += (sample_index,)
            fig_z.data[0].y += (z_new,)
            fig_z.data[1].x += (sample_index,)
            fig_z.data[1].y += (z_moving_avg,)
        
        if z_moving_avg > THRESHOLD_Z:
            # print('alertz')
            send_alert_to_microbit(serial_connection, "Alert Z")

if __name__ == "__main__":
    port = '/dev/tty.usbmodem21402'  # Example for Linux/Mac. Use 'COM#' for Windows.
    read_serial_data(port, duration=15)  # Read data for 10 seconds

