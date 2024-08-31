import streamlit as st
from utils.database import create_user, get_user

def show():
    st.header("Sign Up")
    with st.form("signup_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        contact = st.text_input("Contact")
        age = st.number_input("Age", min_value=18, max_value=120)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        profession = st.text_input("Profession")
        earning = st.number_input("Annual Earning (in USD)", min_value=0)
        insurances = st.multiselect("Types of Insurances Owned", ["Vehicle", "Health", "Life", "Other"])
        investment_mindset = st.slider("Investment Mindset (1: Conservative, 10: Aggressive)", 1, 10)
        investment_experience = st.number_input("Years of Investment Experience", min_value=0)
        previous_investments = st.text_area("Previous Investments (Type, Duration, Quantity)")
        properties = st.text_area("Properties Owned & Current Values")

        if st.form_submit_button("Sign Up"):
            if get_user(email):
                st.error("Email already exists")
            else:
                user_data = {
                    "name": name,
                    "email": email,
                    "password": password,  
                    "contact": contact,
                    "age": age,
                    "gender": gender,
                    "profession": profession,
                    "earning": earning,
                    "insurances": insurances,
                    "investment_mindset": investment_mindset,
                    "investment_experience": investment_experience,
                    "previous_investments": previous_investments,
                    "properties": properties
                }
                result = create_user(user_data)
                if result.inserted_id:
                    st.success("Account created successfully! Please sign in.")
                else:
                    st.error("An error occurred while creating your account. Please try again.")
