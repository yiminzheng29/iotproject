import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from IPython.display import display


st.title('Yoga 101')

picture = st.camera_input("Take a picture")

if picture:
    st.image(picture)
