import streamlit as st

def navbar():
    """Display the navigation bar based on user authentication."""
    # Ensure the 'user' key exists in session_state
    if 'user' not in st.session_state:
        st.session_state['user'] = None

    # Display menu items based on user authentication
    if st.session_state.user:
        menu_items = ["Home", "Chat", "Profile", "Hunt", "Sign Out"]
    else:
        menu_items = ["Home", "Sign In", "Sign Up"]

    selected_page = st.sidebar.radio("Navigate", menu_items)
    return selected_page
