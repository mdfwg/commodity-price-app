import streamlit as st
import requests
from datetime import date
import pandas as pd

# API base URL
API_BASE_URL = "http://localhost:8000"

def price_form_page():
    st.title("📝 Add/Update Price Data")
    st.markdown("Add new price entries or update existing ones")
    
    # Create tabs for Add, Update, and Delete
    tab1, tab2, tab3 = st.tabs(["Add New Price", "Update Price", "Delete Price"])
    
    with tab1:
        add_new_price_form()
    
    with tab2:
        update_price_form()
    
    with tab3:
        delete_price_form()

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
        
        # Created by (get user ID from session state)
        user = st.session_state.get('user')
        created_by = user.id if user else ''
        
        # Submit button
        submit_button = st.form_submit_button("Add Price Entry", type="primary")
        
        if submit_button:
            if not all([selected_region, selected_commodity, selected_date, price, created_by]):
                st.error("Please fill in all required fields.")
            else:
                add_price_entry(selected_region, selected_commodity, selected_date, price, created_by)

def update_price_form():
    st.header("Update Price Entry")
    st.markdown("Select the criteria to find the price entry you want to update")
    
    # Initialize session state for update
    if 'update_search_completed' not in st.session_state:
        st.session_state.update_search_completed = False
    if 'selected_update_id' not in st.session_state:
        st.session_state.selected_update_id = None
    
    # Show search form if not completed
    if not st.session_state.update_search_completed:
        with st.form("update_search_form"):
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
            search_region = st.selectbox("Region", ["All"] + regions, key="search_region")
            
            # Commodity selection
            commodities = [
                "Bawang Merah", "Bawang Putih Bonggol", "Beras Medium", "Beras Premium",
                "Cabai Merah Keriting", "Cabai Rawit Merah", "Daging Ayam Ras",
                "Daging Sapi Murni", "Gula Konsumsi", "Minyak Goreng Curah",
                "Minyak Goreng Kemasan Sederhana", "Telur Ayam Ras", "Tepung Terigu (Curah)"
            ]
            search_commodity = st.selectbox("Commodity", ["All"] + commodities, key="search_commodity")
            
            # Date input
            search_date = st.date_input("Date", value=date.today(), key="search_date")
            
            # Search button
            search_button = st.form_submit_button("Search Price Entries", type="primary")
            
            if search_button:
                search_price_entries(search_region, search_commodity, search_date)
    
    # Show update form if search is completed and ID is selected
    elif st.session_state.selected_update_id:
        show_update_form(st.session_state.selected_update_id)
        
        # Add a button to go back to search
        if st.button("Back to Search", type="secondary"):
            st.session_state.update_search_completed = False
            st.session_state.selected_update_id = None
            st.rerun()

def search_price_entries(region, commodity, search_date):
    try:
        # Build query parameters
        params = {}
        if region and region != "All":
            params['regions'] = [region]
        if commodity and commodity != "All":
            params['commodities'] = [commodity]
        if search_date:
            params['start_date'] = search_date.isoformat()
            params['end_date'] = search_date.isoformat()
        
        # Make API request
        with st.spinner("Searching for price entries..."):
            response = requests.get(f"{API_BASE_URL}/data", params=params)
            
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Convert date strings to datetime
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                # Display found entries
                st.subheader(f"Found {len(df)} price entries")
                
                # Create selection interface
                if 'id' in df.columns:
                    options = []
                    for _, row in df.iterrows():
                        date_str = row.get('date', 'N/A')
                        if date_str is not None and hasattr(date_str, 'strftime'):
                            date_str = date_str.strftime('%Y-%m-%d')
                        option_text = f"ID: {row['id']} | {date_str} | {row.get('region_id', 'N/A')} | {row.get('commodity_id', 'N/A')} | Rp {row.get('price', 0):.2f}"
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
                            st.session_state.selected_update_id = selected_id
                            st.session_state.update_search_completed = True
                            st.rerun()
                    else:
                        st.warning("No price entries found.")
                else:
                    st.warning("No price entries found.")
            else:
                st.warning("No price entries found for the selected criteria.")
                
        else:
            st.error(f"Error searching data: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_update_form(price_id):
    st.subheader(f"Update Price Entry (ID: {price_id})")
    st.info("You can only update the price value. Other fields are for reference only.")
    
    with st.form("update_price_form"):
        # Display current values (read-only)
        st.text_input("Current Region", value="(Will be fetched)", disabled=True)
        st.text_input("Current Commodity", value="(Will be fetched)", disabled=True)
        st.text_input("Current Date", value="(Will be fetched)", disabled=True)
        
        # Price input (only editable field)
        update_price = st.number_input("New Price (Rp) *", min_value=0.0, step=0.01, format="%.2f", key="update_price")
        
        # Updated by (get user ID from session state)
        user = st.session_state.get('user')
        update_created_by = user.id if user else ''
        st.text_input("Updated By", value=update_created_by, disabled=True)
        
        # Submit button
        update_submit = st.form_submit_button("Update Price Entry", type="primary")
        
        if update_submit:
            if update_price > 0:
                update_price_entry(price_id, update_price, update_created_by)
                # Reset session state after successful update
                st.session_state.update_search_completed = False
                st.session_state.selected_update_id = None
            else:
                st.error("Please enter a valid price.")

def delete_price_form():
    st.header("Delete Price Entry")
    st.markdown("Select the criteria to find the price entry you want to delete")
    
    # Initialize session state for delete
    if 'delete_search_completed' not in st.session_state:
        st.session_state.delete_search_completed = False
    if 'selected_delete_id' not in st.session_state:
        st.session_state.selected_delete_id = None
    
    # Show search form if not completed
    if not st.session_state.delete_search_completed:
        with st.form("delete_search_form"):
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
            search_region = st.selectbox("Region", ["All"] + regions, key="delete_search_region")
            
            # Commodity selection
            commodities = [
                "Bawang Merah", "Bawang Putih Bonggol", "Beras Medium", "Beras Premium",
                "Cabai Merah Keriting", "Cabai Rawit Merah", "Daging Ayam Ras",
                "Daging Sapi Murni", "Gula Konsumsi", "Minyak Goreng Curah",
                "Minyak Goreng Kemasan Sederhana", "Telur Ayam Ras", "Tepung Terigu (Curah)"
            ]
            search_commodity = st.selectbox("Commodity", ["All"] + commodities, key="delete_search_commodity")
            
            # Date input
            search_date = st.date_input("Date", value=date.today(), key="delete_search_date")
            
            # Search button
            search_button = st.form_submit_button("Search Price Entries", type="primary")
            
            if search_button:
                search_price_entries_for_delete(search_region, search_commodity, search_date)
    
    # Show delete confirmation if search is completed and ID is selected
    elif st.session_state.selected_delete_id:
        show_delete_confirmation(st.session_state.selected_delete_id)
        
        # Add a button to go back to search
        if st.button("Back to Search", type="secondary", key="delete_back"):
            st.session_state.delete_search_completed = False
            st.session_state.selected_delete_id = None
            st.rerun()

def search_price_entries_for_delete(region, commodity, search_date):
    try:
        # Build query parameters
        params = {}
        if region and region != "All":
            params['regions'] = [region]
        if commodity and commodity != "All":
            params['commodities'] = [commodity]
        if search_date:
            params['start_date'] = search_date.isoformat()
            params['end_date'] = search_date.isoformat()
        
        # Make API request
        with st.spinner("Searching for price entries..."):
            response = requests.get(f"{API_BASE_URL}/data", params=params)
            
        if response.status_code == 200:
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                
                # Convert date strings to datetime
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                # Display found entries
                st.subheader(f"Found {len(df)} price entries")
                
                # Create selection interface
                if 'id' in df.columns:
                    options = []
                    for _, row in df.iterrows():
                        date_str = row.get('date', 'N/A')
                        if date_str is not None and hasattr(date_str, 'strftime'):
                            date_str = date_str.strftime('%Y-%m-%d')
                        option_text = f"ID: {row['id']} | {date_str} | {row.get('region_id', 'N/A')} | {row.get('commodity_id', 'N/A')} | Rp {row.get('price', 0):.2f}"
                        options.append((row['id'], option_text))
                    
                    if options:
                        selected_option = st.selectbox(
                            "Choose entry to delete:",
                            options=[opt[1] for opt in options],
                            key="delete_selection"
                        )
                        
                        # Get the selected ID
                        selected_id = None
                        for opt_id, opt_text in options:
                            if opt_text == selected_option:
                                selected_id = opt_id
                                break
                        
                        if selected_id:
                            st.session_state.selected_delete_id = selected_id
                            st.session_state.delete_search_completed = True
                            st.rerun()
                    else:
                        st.warning("No price entries found.")
                else:
                    st.warning("No price entries found.")
            else:
                st.warning("No price entries found for the selected criteria.")
                
        else:
            st.error(f"Error searching data: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def show_delete_confirmation(price_id):
    st.subheader(f"Delete Price Entry (ID: {price_id})")
    st.warning("⚠️ This action cannot be undone!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Cancel", type="secondary", key="delete_cancel"):
            st.session_state.delete_search_completed = False
            st.session_state.selected_delete_id = None
            st.rerun()
    
    with col2:
        if st.button("Delete Entry", type="primary", key="delete_confirm"):
            delete_price_entry(price_id)
            # Reset session state after successful deletion
            st.session_state.delete_search_completed = False
            st.session_state.selected_delete_id = None

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

def update_price_entry(price_id, price, created_by):
    try:
        payload = {
            "price": price,
            "created_by": created_by
        }
        
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

def delete_price_entry(price_id):
    try:
        with st.spinner("Deleting price entry..."):
            response = requests.delete(f"{API_BASE_URL}/data/{price_id}")
        
        if response.status_code == 200:
            st.success("Price entry deleted successfully!")
            st.json(response.json())
        else:
            st.error(f"Error deleting price entry: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}") 