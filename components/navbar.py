import streamlit as st

def navbar():
    if st.session_state.user:
        menu_items = ["Home", "Chat", "Profile", "Hunt", "Sign Out"]
    else:
        menu_items = ["Home", "Sign In", "Sign Up"]

    selected = st.sidebar.selectbox("Navigation", menu_items)
    
    return selected