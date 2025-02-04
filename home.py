import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
from openai import OpenAI
from dotenv import load_dotenv


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



