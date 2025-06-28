# frontend/helpers/auth.py
import streamlit as st
from backend.supabase_client import supabase

def login(email: str, password: str) -> bool:
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # Store whole user session in st.session_state
        st.session_state["user"] = auth_response
        st.session_state["user_id"] = auth_response.user.id
        st.session_state["access_token"] = auth_response.session.access_token

        # (Optional) Fetch role from `users` table
        user_info = supabase.table("users").select("role").eq("id", auth_response.user.id).single().execute()
        st.session_state["user_role"] = user_info.data["role"]

        return True
    except Exception as e:
        st.error(f"Login failed: {e}")
        return False

def logout():
    for key in ["user", "user_id", "access_token", "user_role"]:
        st.session_state.pop(key, None)
    st.success("You have been logged out.")