import streamlit as st
from utils.database import update_user

def show():
    if not st.session_state.user:
        st.warning("Please sign in to view your profile.")
        return

    st.header("Your Profile")
    user = st.session_state.user

    with st.form("profile_form"):
        name = st.text_input("Name", user["name"])
        email = st.text_input("Email", user["email"], disabled=True)
        contact = st.text_input("Contact", user["contact"])
        age = st.number_input("Age", min_value=18, max_value=120, value=user["age"])
        gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(user["gender"]))
        profession = st.text_input("Profession", user["profession"])
        earning = st.number_input("Annual Earning (in USD)", min_value=0, value=user["earning"])
        insurances = st.multiselect("Types of Insurances Owned", ["Vehicle", "Health", "Life", "Other"], default=user["insurances"])
        investment_mindset = st.slider("Investment Mindset (1: Conservative, 10: Aggressive)", 1, 10, value=user["investment_mindset"])
        investment_experience = st.number_input("Years of Investment Experience", min_value=0, value=user["investment_experience"])
        previous_investments = st.text_area("Previous Investments (Type, Duration, Quantity)", user["previous_investments"])
        properties = st.text_area("Properties Owned & Current Values", user["properties"])

        # Add the new field for owned stocks
        owned_stocks = st.text_area("Owned Stocks (comma-separated)", ", ".join(user.get("owned_stocks", [])))

        if st.form_submit_button("Update Profile"):
            updated_data = {
                "name": name,
                "contact": contact,
                "age": age,
                "gender": gender,
                "profession": profession,
                "earning": earning,
                "insurances": insurances,
                "investment_mindset": investment_mindset,
                "investment_experience": investment_experience,
                "previous_investments": previous_investments,
                "properties": properties,
                "owned_stocks": [stock.strip() for stock in owned_stocks.split(",") if stock.strip()]
            }
            update_user(email, updated_data)
            st.session_state.user.update(updated_data)
            st.success("Profile updated successfully!")
