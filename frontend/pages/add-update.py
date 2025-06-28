# frontend/pages/3_Add_or_Update.py
import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

def add_price():
    st.title("Add or Update Price")

    d = st.date_input("Date", value=date.today())
    region = st.selectbox("Region", options=["Aceh", "Sumatera Utara", ...])
    commodity = st.selectbox("Commodity", options=["Bawang Merah", "Beras Medium", ...])
    price = st.number_input("Price", step=100.0)

    if st.button("Submit"):
        payload = {
            "date": str(d),
            "region": region,
            "commodity": commodity,
            "price": price,
            "created_by": st.session_state["user"]["user"]["id"]  # from login session
        }
        res = requests.post(f"{API_BASE}/data", json=payload)
        if res.status_code == 200:
            st.success("Data submitted.")
        else:
            st.error(f"Failed: {res.text}")

if st.session_state.get("user_role") not in ["admin", "surveyor"]:
    st.error("Access denied.")
else:
    add_price()
