import streamlit as st
from backend.supabase_client import supabase

def login():
    st.title("Login Page")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state["user"] = user
            st.success("Logged in")
            st.switch_page("pages/2_Dashboard.py")
        except Exception as e:
            st.error(f"Login failed: {e}")

if "user" not in st.session_state:
    login()
else:
    st.success("You are already logged in.")