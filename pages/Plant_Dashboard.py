import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import os

# Clear History Function
def clear_history():
    global growth_data
    growth_data = pd.DataFrame(columns=["Date", "Plant", "Classroom", "Growth_cm"])
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.experimental_rerun()

# App Layout
st.set_page_config(page_title="Plant Project Dashboard", layout="wide")
st.title("🌼🏫 RBMS HH Growth Project")

# Persistent Data File
DATA_FILE = "plant_growth_data.csv"

# Load persistent data
if os.path.exists(DATA_FILE):
    growth_data = pd.read_csv(DATA_FILE)
    growth_data["Date"] = pd.to_datetime(growth_data["Date"]).dt.date
else:
    growth_data = pd.DataFrame(columns=["Date", "Plant", "Classroom", "Growth_cm"])


# Sidebar Authentication
if "user_authenticated" not in st.session_state:
    st.session_state["user_authenticated"] = False

# Sidebar Tools
if not st.session_state["user_authenticated"]:
    st.sidebar.header("Sign In")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Sign In"):
        if username == "admin" and password == "password":  # Replace with a secure authentication method
            st.session_state["user_authenticated"] = True
            st.sidebar.success("Welcome!")
        else:
            st.sidebar.error("Invalid credentials. Please try again.")

if st.session_state["user_authenticated"]:
    st.sidebar.header("Add New Plant Growth Data")

    date = st.sidebar.date_input("Date")
    plant_name = st.sidebar.selectbox("Plant Name", ["Plant A", "Plant B", "Plant C", "Plant D"])
    classroom_numbers = [2210, 2101, 1101, 3309]
    classroom_number = st.sidebar.selectbox("Classroom Number", options=classroom_numbers)
    growth_cm = st.sidebar.number_input("Growth (cm)", min_value=0.0, step=0.1)

    if st.sidebar.button("Submit Data"):
        new_entry = pd.DataFrame({
            "Date": [date],
            "Plant": [plant_name],
            "Classroom": [classroom_number],
            "Growth_cm": [growth_cm]
        })
        growth_data = pd.concat([growth_data, new_entry], ignore_index=True)
        growth_data.to_csv(DATA_FILE, index=False)
        st.sidebar.success(f"Data for {plant_name} in Classroom {classroom_number} added successfully!")

    # Clear History Button
    if st.sidebar.button("Clear History"):
        clear_history()

    # Sign Out Button
    if st.sidebar.button("Sign Out"):
        st.session_state["user_authenticated"] = False
        st.experimental_rerun()




# Main Page Content
st.write("### Plant Growth Tracking")
st.write("This dashboard visualizes plant growth data and allows for tracking monthly progress.")
with st.expander("View Plant Growth Data", expanded=False):
    if not growth_data.empty:
        st.dataframe(growth_data)
    else:
        st.write("No data available.")
st.markdown("---", unsafe_allow_html=True)
st.write("## Growth Dashboard")
if "start_date" not in st.session_state:
    st.session_state["start_date"] = datetime.now().replace(day=1).date()

start_date = st.session_state["start_date"]
end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
st.write(f"### Tracking Month: {start_date.strftime('%B %Y')}")

col1, col2 = st.columns(2)
with col1:
    if st.button("Previous Month"):
        st.session_state["start_date"] = (start_date - timedelta(days=1)).replace(day=1)
with col2:
    if st.button("Next Month"):
        st.session_state["start_date"] = (end_date + timedelta(days=1)).replace(day=1)

monthly_data = growth_data[(growth_data["Date"] >= start_date) & (growth_data["Date"] <= end_date)]

if not monthly_data.empty:
    current_month_growth = monthly_data["Growth_cm"].sum()
    unit = st.selectbox("Select Unit:", ["cm", "ft"])

    if unit == "ft":
        current_month_growth_display = current_month_growth / 30.48  # Convert cm to ft
    else:
        current_month_growth_display = current_month_growth

    st.write(f"#### Total Growth ({unit}): {current_month_growth_display:.2f}")

    previous_months_data = growth_data[growth_data["Date"] < start_date]
    total_previous_growth = previous_months_data["Growth_cm"].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar("Current Month", current_month_growth_display, color="green", label=f"Current Month Growth ({unit})")
    ax.bar("Total Growth", (current_month_growth + total_previous_growth) / (30.48 if unit == "ft" else 1),
            color="blue", label=f"Total Growth ({unit})")

    ax.set_title("Growth Metrics: Current Month and Total")
    ax.set_ylabel(f"Growth ({unit})")
    ax.legend()
    st.pyplot(fig)
else:
    st.write("No growth data for this month.")