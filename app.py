import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# App Layout
st.set_page_config(page_title="School Growth Dashboard", layout="wide")

# File-based persistence
DATA_FILE = "growth_data.csv"

# Load or initialize growth data
if os.path.exists(DATA_FILE):
    growth_data = pd.read_csv(DATA_FILE, parse_dates=["Date"])
else:
    growth_data = pd.DataFrame(columns=["Date", "Classroom", "Growth_cm"])

# Sidebar Inputs
st.sidebar.header("Growth SideBar")

date = st.sidebar.date_input("Date")
classroom_number = st.sidebar.selectbox("Classroom #", options=[1001, 1002, 1003, 1004])
growth_cm = st.sidebar.number_input("Growth in cm", min_value=0.0, step=0.1)

if st.sidebar.button("Submit"):
    # Add data to the DataFrame
    new_entry = pd.DataFrame({
        "Date": [date],
        "Classroom": [classroom_number],
        "Growth_cm": [growth_cm]
    })
    growth_data = pd.concat([growth_data, new_entry], ignore_index=True)
    growth_data.to_csv(DATA_FILE, index=False)
    st.sidebar.success(f"Data submitted! Classroom: {classroom_number}, Date: {date}, Growth: {growth_cm} cm")

# History Section in Sidebar
st.sidebar.subheader("History")
st.sidebar.text_area(
    "Previous entries",
    value=growth_data[["Date", "Classroom", "Growth_cm"]].to_string(index=False),
    height=800
)

# Delete History Functionality
if st.sidebar.button("Clear History"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    growth_data = pd.DataFrame(columns=["Date", "Classroom", "Growth_cm"])
    st.sidebar.success("All history and data cleared successfully!")

