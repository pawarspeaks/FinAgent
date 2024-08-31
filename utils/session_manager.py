import streamlit as st
import uuid

def init_session():
    """Initialize the session if it doesn't exist."""
    if 'session_id' not in st.session_state:
        st.session_state['session_id'] = str(uuid.uuid4())
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

def set_session_cookie():
    """Set the session cookie in the session state."""
    if 'session_id' in st.session_state:
        st.session_state['session_cookie'] = st.session_state['session_id']

def clear_session():
    """Clear the session state."""
    st.session_state.clear()
