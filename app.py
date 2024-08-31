import streamlit as st
from components.navbar import navbar
from utils.session_manager import init_session, set_session_cookie, clear_session
import pages.signin as signin
import pages.signup as signup
import pages.profile as profile
import pages.chat as chat
from pages import hunt
from openai import OpenAI
import os
from utils.finbert_helper import analyze_financial_text

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response_func(user_input):
    """Generate response from GPT and analyze text with FinBERT."""
    try:
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "system", "content": "You are a helpful financial assistant."}
            ]
        
        user_context = get_user_context()
        finbert_analysis = analyze_financial_text(user_input)
        full_prompt = f"{user_context}\n\nUser: {user_input}\n\nFinBERT Analysis: {finbert_analysis}"
        st.session_state.messages.append({"role": "user", "content": full_prompt})

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        
        response_message = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": response_message})
        
        return f"GPT Response: {response_message}\n\nFinBERT Analysis: {finbert_analysis}"
    except KeyError as e:
        return f"KeyError: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_user_context():
    """Retrieve user context for personalized responses."""
    if "user" in st.session_state and st.session_state.user:
        user = st.session_state.user
        return f"""User Profile:
        Name: {user.get('name', 'N/A')}
        Email: {user.get('email', 'N/A')}
        Age: {user.get('age', 'N/A')}
        Gender: {user.get('gender', 'N/A')}
        Profession: {user.get('profession', 'N/A')}
        Annual Earning: ${user.get('earning', 'N/A')}
        Insurances: {', '.join(user.get('insurances', []))}
        Investment Mindset: {user.get('investment_mindset', 'N/A')}/10
        Investment Experience: {user.get('investment_experience', 'N/A')} years
        Previous Investments: {user.get('previous_investments', 'N/A')}
        Properties: {user.get('properties', 'N/A')}
        """
    return "No user context available."

st.set_page_config(page_title="FinAgent360", layout="wide", menu_items={"Get Help": None, "Report a bug": None, "About": None})

def main():
    """Main function to handle page navigation and session management."""
    st.title("FinAgent360")

    init_session()
    selected_page = navbar()

    if selected_page == "Sign Out":
        clear_session()
        st.success("Signed out successfully!")
        selected_page = "Home"

    if selected_page == "Home":
        st.write("Welcome to FinAgent360!")
    elif selected_page == "Sign In" and st.session_state.user is None:
        signin.show()
    elif selected_page == "Sign Up" and st.session_state.user is None:
        signup.show()
    elif selected_page == "Profile" and st.session_state.user:
        profile.show()
    elif selected_page == "Chat" and st.session_state.user:
        chat.show()
    elif selected_page == "Hunt" and st.session_state.user:
        hunt.show()

    if st.session_state.user:
        set_session_cookie()

if __name__ == "__main__":
    main()
