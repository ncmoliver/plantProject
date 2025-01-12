import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv('secrets.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

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

# Clear History Function
def clear_history():
    global growth_data
    growth_data = pd.DataFrame(columns=["Date", "Plant", "Classroom", "Growth_cm"])
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    st.experimental_rerun()

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

# Tabs Section
tabs = st.tabs(["About Project","Dashboard","Affirmations", "Types of Plants", "Plant Locations"])

with tabs[0]:
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/welcome.jpeg", width=500)
        st.caption("Helping Hands | River Bend Middle School | Raleigh, NC")
    with col2:
        st.write("### About the Helping Hands Plant Project")
        st.write("### Objectives:")
        st.markdown(
            """
            - Create a calming, inspiring environment for students.
            - Teach students about responsibility through plant care.
            - Monitor and celebrate plant growth as a community effort.
            """
        )
        with st.expander("### HH Student Creators"):
            student = st.segmented_control("Student Creators", options=["George", "Rodriguez", "Chembi"])
            if student == "George":
                st.image("images/creators/george.jpeg", width=500)
            if student == "Rodriguez":
                st.image("images/creators/rodriguez.jpeg", width=500)
            if student == "Chembi":
                st.image("images/creators/chembi.jpeg", width=500)
with tabs[1]:
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
with tabs[2]:
    st.subheader("Affirmations")
    col1, col2 = st.columns(2)
    with col1:
        affirmation_type = st.selectbox("Select Affirmation Type", ["Growth Mindset", "Belief", "Hope", "Encouragement", "Happiness", "Helping", "Receiving"])
    with col2:
        mood = st.selectbox("Mood", options=["Happy", "Sad", "Sleepy", "Opportunistic", "Imaginative", "Creative", "Dull", "Bored"])
    plant_types = ["Lillies", "Snake Plants", "Roses"]
    affirmation_btn = st.button("Get Affirmation")
    if affirmation_btn:
        with st.spinner("Getting Affirmation..."):

            client = OpenAI(
                organization='org-NjWeuyfFqgkukpzWoctKmLxw',
                project='',
                api_key=openai_api_key
            )
            prompt = [
                {"role": "assistant", "content":f"Your job is to create a unique affirmation with the goal of uplifting middle school aged students morale based on their interest. The affirmations should be creative, easy to read, empowering, and based on life lessons."},
                 {"role": "user", "content":f"User affirmation type requested: {affirmation_type} and mood selected: {mood}"},
            ]
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=prompt,
            )
            affirmation_result = completion.choices[0].message.content
            image_prompt = f"""
                1. Create a image based on our school project to boost middle school aged students morale based on the following affirmation: {affirmation_result}.
                2. Use the {mood} and {affirmation_result} of the image to create a image that tells a uplifting story.
                3. NO words, just the image only.
            """
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            image_result = response.data[0].url
            st.markdown(f"##### {affirmation_result}", unsafe_allow_html=True)
            st.image(image_result)

with tabs[3]:
    st.subheader("🏗️ Plant Benefits & Maintenance")
    st.write("On this page, you can design a custom page tailored to your preferred plant type and page style. Give it a try! 😊")
    plant_types = {
        "Lillies": "images/lillies.jpeg",
        "Snake Plants": "images/snake_plant.jpeg",
        "Roses": "images/roses.jpeg"
    }

    col1, col2 = st.columns(2)
    with col1:
        selected_plant = st.selectbox("Select Plant Type:", list(plant_types.keys()))
    with col2:
        page_style = st.selectbox("Page style", ["Informative", "Happy", "Cool, yet mannered", "Respectful"])
    plant_submit_btn = st.button("Get Plant Info")
    if plant_submit_btn:
        with st.spinner("Getting Custom Plant Info..."):
            img_path = plant_types[selected_plant]

            st.markdown("---", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader(selected_plant)
                st.image(img_path, caption=selected_plant, width=500)
            with col2:
                client = OpenAI(
                    organization='',
                    project='',
                    api_key=openai_api_key,
                )

                prompt = {
                    "role": "assistant",
                    "content": f"""
                        1. Act as a plant enthusiast and explain one unique benefit of the {selected_plant} in concise, a easy to ready, markdown format, including emojis, under Benfits of {selected_plant}.
                        2. Paragraph 2 is on Plant Maintenance: Include simple, short, monthly maintenance schedule on how to care for the following plant in a list format, choose top 5 most important: {selected_plant}.
                        3. Customize the page style toward the suggest writing style: {page_style}
                        4. Two separate paragraphs, one for plant benefits, the other on plant maintenance and care. No boilerplate introduction, just response in an organized markdown format.
                        5. Use simple words.
                        """,
                }
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[prompt]
                )
                with st.spinner(f"Retrieving updated data on {plant_types[selected_plant]}..."):
                    response = completion.choices[0].message.content
                    st.markdown(response, unsafe_allow_html=True)

with tabs[4]:
    st.subheader("Plant Locations")

    if not growth_data.empty:
        classrooms = growth_data["Classroom"].unique()
        selected_classroom = st.selectbox("Select Classroom:", classrooms)

        class_data = growth_data[growth_data["Classroom"] == selected_classroom]
        plant_types = class_data["Plant"].unique()
        total_growth = class_data["Growth_cm"].sum()

        st.write(f"### Classroom {selected_classroom}")
        st.markdown(
            f"""
            <div style="color:red font-size: 20px">
                <p><strong>Plant Types:</strong> <span>{', '.join(plant_types)}<span></p>
                <p><strong>Total Growth:</strong> <span>{total_growth:.2f}<span> cm</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.image(f"images/classroom_{selected_classroom}.jpg", caption=f"Classroom {selected_classroom}", width=500)
    else:
        st.write("No plant data available.")
