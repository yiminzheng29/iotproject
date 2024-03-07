import streamlit as st
from streamlit_webcam import st_webcam
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
#from IPython.display import display


st.title('Yoga 101')

st_webcam(key="webcam")
