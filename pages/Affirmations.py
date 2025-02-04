import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv('secrets.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

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