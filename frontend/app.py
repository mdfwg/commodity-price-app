import streamlit as st
from auth_page import auth_page
from dashboard_page import dashboard_page
from price_form_page import price_form_page

# Page configuration
st.set_page_config(
    page_title="Commodity Price App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    # Main header
    st.markdown('<h1 class="main-header">🏪 Commodity Price Management System</h1>', unsafe_allow_html=True)
    
    # Check authentication first
    if not st.session_state.authenticated:
        # Show authentication page
        auth_page()
        return
    
    # If authenticated, store user email for forms
    if st.session_state.user and hasattr(st.session_state.user, 'email'):
        st.session_state.user_email = st.session_state.user.email
    
    # Navigation sidebar
    st.sidebar.title("Navigation")
    
    # User info in sidebar
    if st.session_state.user_email:
        st.sidebar.success(f"Logged in as: {st.session_state.user_email}")
    
    # Navigation options
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Dashboard", "Add/Update Prices", "Logout"]
    )
    
    # Page routing
    if page == "Dashboard":
        dashboard_page()
    elif page == "Add/Update Prices":
        price_form_page()
    elif page == "Logout":
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.user_email = None
        st.success("Logged out successfully!")
        st.rerun()

if __name__ == "__main__":
    main() 