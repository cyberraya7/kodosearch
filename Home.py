import sys
import os
import streamlit as st

#from phoneintel.app import main as phoneintel_main
from kizunafinder.app import main as kizunafinder_main
from ferb.app import main as ferb_main

# Set page configuration
st.set_page_config(page_title="Multi-Tool App", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
app_selection = st.sidebar.selectbox(
    "Select an App", 
    ["Select", "Phone Validation Application", "Social Media Search Application"]
)

# Render the selected app
if app_selection == "Phone Validation Application":
    ferb_main()
elif app_selection == "Social Media Search Application":
    kizunafinder_main()
else:
    st.write("Please select an app from the dropdown.")
