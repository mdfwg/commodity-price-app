import streamlit as st
import requests
from datetime import date
import pandas as pd

# API base URL
API_BASE_URL = "http://localhost:8000"

def price_form_page():
    st.title("📝 Add/Update Price Data")
    st.markdown("Add new price entries or update existing ones")
    
    # Create tabs for Add and Update
    tab1, tab2 = st.tabs(["Add New Price", "Update Price"])
    
    with tab1:
        add_new_price_form()
    
    with tab2:
        update_price_form()

def add_new_price_form():
    st.header("Add New Price Entry")
    
    with st.form("add_price_form"):
        # Region selection
        regions = [
            "Aceh", "Bali", "Banten", "Bengkulu", "DI Yogyakarta", "DKI Jakarta",
            "Gorontalo", "Jambi", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
            "Kalimantan Barat", "Kalimantan Selatan", "Kalimantan Tengah",
            "Kalimantan Timur", "Kalimantan Utara", "Kepulauan Bangka Belitung",
            "Kepulauan Riau", "Lampung", "Maluku", "Maluku Utara",
            "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Papua", "Papua Barat",
            "Riau", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tengah",
            "Sulawesi Tenggara", "Sulawesi Utara", "Sumatera Barat",
            "Sumatera Selatan", "Sumatera Utara"
        ]
        selected_region = st.selectbox("Region *", regions)
        
        # Commodity selection
        commodities = [
            "Bawang Merah", "Bawang Putih Bonggol", "Beras Medium", "Beras Premium",
            "Cabai Merah Keriting", "Cabai Rawit Merah", "Daging Ayam Ras",
            "Daging Sapi Murni", "Gula Konsumsi", "Minyak Goreng Curah",
            "Minyak Goreng Kemasan Sederhana", "Telur Ayam Ras", "Tepung Terigu (Curah)"
        ]
        selected_commodity = st.selectbox("Commodity *", commodities)
        
        # Date input
        selected_date = st.date_input("Date *", value=date.today())
        
        # Price input
        price = st.number_input("Price (Rp) *", min_value=0.0, step=0.01, format="%.2f")
        
        # Created by (get from session state if available)
        created_by = st.text_input("Created By *", value=st.session_state.get('user_email', ''))
        
        # Submit button
        submit_button = st.form_submit_button("Add Price Entry", type="primary")
        
        if submit_button:
            if not all([selected_region, selected_commodity, selected_date, price, created_by]):
                st.error("Please fill in all required fields.")
            else:
                add_price_entry(selected_region, selected_commodity, selected_date, price, created_by)

def update_price_form():
    st.header("Update Price Entry")
    
    # First, let user select a price entry to update
    st.subheader("Select Price Entry to Update")
    
    # Fetch recent data for selection
    try:
        response = requests.get(f"{API_BASE_URL}/data")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                
                # Create a selection interface
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date']).dt.date
                
                # Show recent entries for selection
                st.write("Recent price entries:")
                display_df = df.head(20).copy()  # Show last 20 entries
                
                # Create a selection box with formatted entries
                if 'id' in display_df.columns:
                    options = []
                    for _, row in display_df.iterrows():
                        option_text = f"ID: {row['id']} | {row.get('date', 'N/A')} | {row.get('region_id', 'N/A')} | {row.get('commodity_id', 'N/A')} | Rp {row.get('price', 0):.2f}"
                        options.append((row['id'], option_text))
                    
                    if options:
                        selected_option = st.selectbox(
                            "Choose entry to update:",
                            options=[opt[1] for opt in options],
                            key="update_selection"
                        )
                        
                        # Get the selected ID
                        selected_id = None
                        for opt_id, opt_text in options:
                            if opt_text == selected_option:
                                selected_id = opt_id
                                break
                        
                        if selected_id:
                            show_update_form(selected_id)
                    else:
                        st.warning("No price entries found.")
                else:
                    st.warning("No price entries found.")
            else:
                st.warning("No data available for updating.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_update_form(price_id):
    st.subheader(f"Update Price Entry (ID: {price_id})")
    
    with st.form("update_price_form"):
        # Region selection
        regions = [
            "Aceh", "Bali", "Banten", "Bengkulu", "DI Yogyakarta", "DKI Jakarta",
            "Gorontalo", "Jambi", "Jawa Barat", "Jawa Tengah", "Jawa Timur",
            "Kalimantan Barat", "Kalimantan Selatan", "Kalimantan Tengah",
            "Kalimantan Timur", "Kalimantan Utara", "Kepulauan Bangka Belitung",
            "Kepulauan Riau", "Lampung", "Maluku", "Maluku Utara",
            "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Papua", "Papua Barat",
            "Riau", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tengah",
            "Sulawesi Tenggara", "Sulawesi Utara", "Sumatera Barat",
            "Sumatera Selatan", "Sumatera Utara"
        ]
        update_region = st.selectbox("Region", ["Keep current"] + regions, key="update_region")
        
        # Commodity selection
        commodities = [
            "Bawang Merah", "Bawang Putih Bonggol", "Beras Medium", "Beras Premium",
            "Cabai Merah Keriting", "Cabai Rawit Merah", "Daging Ayam Ras",
            "Daging Sapi Murni", "Gula Konsumsi", "Minyak Goreng Curah",
            "Minyak Goreng Kemasan Sederhana", "Telur Ayam Ras", "Tepung Terigu (Curah)"
        ]
        update_commodity = st.selectbox("Commodity", ["Keep current"] + commodities, key="update_commodity")
        
        # Date input
        update_date = st.date_input("Date", value=date.today(), key="update_date")
        
        # Price input
        update_price = st.number_input("Price (Rp)", min_value=0.0, step=0.01, format="%.2f", key="update_price")
        
        # Created by
        update_created_by = st.text_input("Updated By", value=st.session_state.get('user_email', ''), key="update_created_by")
        
        # Submit button
        update_submit = st.form_submit_button("Update Price Entry", type="primary")
        
        if update_submit:
            update_price_entry(price_id, update_region, update_commodity, update_date, update_price, update_created_by)

def add_price_entry(region, commodity, date_val, price, created_by):
    try:
        payload = {
            "region": region,
            "commodity": commodity,
            "date": date_val.isoformat(),
            "price": price,
            "created_by": created_by
        }
        
        with st.spinner("Adding price entry..."):
            response = requests.post(f"{API_BASE_URL}/data", json=payload)
        
        if response.status_code == 200:
            st.success("Price entry added successfully!")
            st.json(response.json())
        else:
            st.error(f"Error adding price entry: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def update_price_entry(price_id, region, commodity, date_val, price, created_by):
    try:
        payload = {}
        
        if region != "Keep current":
            payload["region"] = region
        if commodity != "Keep current":
            payload["commodity"] = commodity
        if date_val:
            payload["date"] = date_val.isoformat()
        if price > 0:
            payload["price"] = price
        if created_by:
            payload["created_by"] = created_by
        
        if not payload:
            st.warning("No changes to update.")
            return
        
        with st.spinner("Updating price entry..."):
            response = requests.put(f"{API_BASE_URL}/data/{price_id}", json=payload)
        
        if response.status_code == 200:
            st.success("Price entry updated successfully!")
            st.json(response.json())
        else:
            st.error(f"Error updating price entry: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 