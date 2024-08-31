import streamlit as st
from utils.database import verify_user

def show():
    st.header("Sign In")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if 'sign_in_clicked' not in st.session_state:
        st.session_state.sign_in_clicked = False

    def on_sign_in_click():
        st.session_state.sign_in_clicked = True

    # Button triggers the on_sign_in_click function
    st.button("Sign In", on_click=on_sign_in_click)

    # Handle the sign-in logic
    if st.session_state.sign_in_clicked:
        user = verify_user(email, password)
        if user:
            st.session_state.user = user
            st.success("Signed in successfully!")
            st.session_state.sign_in_clicked = False  # Reset the button state
        else:
            st.error("Invalid email or password")
            st.session_state.sign_in_clicked = False  # Reset the button state
