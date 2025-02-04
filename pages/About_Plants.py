import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('secrets.env')
openai_api_key = os.getenv('OPENAI_API_KEY')


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