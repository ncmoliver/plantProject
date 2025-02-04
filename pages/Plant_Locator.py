import streamlit as st

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