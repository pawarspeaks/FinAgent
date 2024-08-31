import streamlit as st
from components.chat_interface import chat_interface
from utils.openai_helper import get_gpt3_response

def show():
    if not st.session_state.user:
        st.warning("Please sign in to use the chat feature.")
        return

    st.header("Chat with FinAgent360")

    def get_user_context():
        user = st.session_state.user
        return f"""User Profile:
        Name: {user['name']}
        Email: {user['email']}
        Age: {user['age']}
        Gender: {user['gender']}
        Profession: {user['profession']}
        Annual Earning: ${user['earning']}
        Insurances: {', '.join(user['insurances'])}
        Investment Mindset: {user['investment_mindset']}/10
        Investment Experience: {user['investment_experience']} years
        Previous Investments: {user['previous_investments']}
        Properties: {user['properties']}
        """

    def get_response(prompt):
        user_context = get_user_context()
        return get_gpt3_response(prompt, user_context)

    chat_interface(get_response)