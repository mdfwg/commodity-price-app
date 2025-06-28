import streamlit as st
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    st.error("Missing Supabase configuration. Please check your environment variables.")
    st.stop()

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def auth_page():
    st.title("🔐 Authentication")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Check if user is already authenticated
    if st.session_state.authenticated and st.session_state.user:
        st.success(f"Welcome back, {st.session_state.user.email}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.rerun()
        return True
    
    # Create tabs for login and signup
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email", type="default")
            password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Login")
            
            if submit_login:
                if email and password:
                    try:
                        response = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        if response.user:
                            st.session_state.authenticated = True
                            st.session_state.user = response.user
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Login failed. Please check your credentials.")
                    except Exception as e:
                        st.error(f"Login error: {str(e)}")
                else:
                    st.error("Please fill in all fields.")
    
    with tab2:
        st.header("Sign Up")
        with st.form("signup_form"):
            signup_email = st.text_input("Email", key="signup_email", type="default")
            signup_password = st.text_input("Password", key="signup_password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit_signup = st.form_submit_button("Sign Up")
            
            if submit_signup:
                if signup_email and signup_password and confirm_password:
                    if signup_password != confirm_password:
                        st.error("Passwords do not match.")
                    elif len(signup_password) < 6:
                        st.error("Password must be at least 6 characters long.")
                    else:
                        try:
                            response = supabase.auth.sign_up({
                                "email": signup_email,
                                "password": signup_password
                            })
                            if response.user:
                                st.success("Account created successfully! Please check your email for verification.")
                            else:
                                st.error("Sign up failed. Please try again.")
                        except Exception as e:
                            st.error(f"Sign up error: {str(e)}")
                else:
                    st.error("Please fill in all fields.")
    
    return False 