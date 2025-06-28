import streamlit as st
import pandas as pd
import requests

API_BASE = "http://localhost:8000"

def dashboard():
    st.title("Dashboard")

    # Filters
    region = st.selectbox("Region", options=["", "Aceh", "Sumatera Utara", ...])
    commodity = st.selectbox("Commodity", options=["", "Bawang Merah", "Beras Medium", ...])
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")

    params = {}
    if region: params["region_id"] = region
    if commodity: params["commodity_id"] = commodity
    if start_date: params["start_date"] = str(start_date)
    if end_date: params["end_date"] = str(end_date)

    # Fetch from FastAPI
    res = requests.get(f"{API_BASE}/data", params=params)
    df = pd.DataFrame(res.json())

    st.dataframe(df)

    st.download_button("Download CSV", df.to_csv(index=False), file_name="prices.csv")

    # Role-based form button
    if st.session_state.get("user_role") in ["admin", "surveyor"]:
        if st.button("Add / Update Price"):
            st.switch_page("pages/3_Add_or_Update.py")

if "user" not in st.session_state:
    st.error("Please log in first.")
else:
    dashboard()
