import streamlit as st
import pandas as pd
import requests
from datetime import date, datetime
import io
import sys
import os

# Add backend directory to path for importing id_mapping
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

# API base URL
API_BASE_URL = "http://localhost:8000"

# Try to import plotly, but don't fail if not available
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    st.warning("Plotly not available. Install with: pip install plotly")

# Try to import the mapping dictionaries
try:
    from id_mapping import region_map, commodity_map
    # Create reverse mappings for display
    region_id_to_name = {v: k for k, v in region_map.items()}
    commodity_id_to_name = {v: k for k, v in commodity_map.items()}
except ImportError:
    st.error("Could not import id_mapping. Make sure the backend directory is accessible.")
    region_map = {}
    commodity_map = {}
    region_id_to_name = {}
    commodity_id_to_name = {}

def dashboard_page():
    st.title("📊 Price Dashboard")
    st.markdown("View and analyze commodity price data")
    st.write(st.session_state)
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Date filters
    st.sidebar.subheader("Date Range")
    start_date = st.sidebar.date_input(
        "Start Date",
        value=date.today().replace(day=1),  # First day of current month
        max_value=date.today()
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=date.today(),
        max_value=date.today()
    )
    
    # Region filter - multi-select
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
    selected_regions = st.sidebar.multiselect("Regions", regions, default=regions[:5])
    
    # Commodity filter - multi-select
    commodities = [
        "Bawang Merah", "Bawang Putih Bonggol", "Beras Medium", "Beras Premium",
        "Cabai Merah Keriting", "Cabai Rawit Merah", "Daging Ayam Ras",
        "Daging Sapi Murni", "Gula Konsumsi", "Minyak Goreng Curah",
        "Minyak Goreng Kemasan Sederhana", "Telur Ayam Ras", "Tepung Terigu (Curah)"
    ]
    selected_commodities = st.sidebar.multiselect("Commodities", commodities, default=commodities[:5])
    
    # Fetch data button
    if st.sidebar.button("Fetch Data", type="primary"):
        fetch_and_display_data(start_date, end_date, selected_regions, selected_commodities)
    
    # Auto-fetch on page load
    if 'data_fetched' not in st.session_state:
        fetch_and_display_data(start_date, end_date, selected_regions, selected_commodities)

def fetch_and_display_data(start_date, end_date, regions, commodities):
    try:
        # Build query parameters
        params = {}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        
        # Add selected regions and commodities to API request
        if regions:
            params['regions'] = regions
        if commodities:
            params['commodities'] = commodities
        
        # Set a higher limit to get more data
        params['limit'] = 50000  # Increased from default 10000
        
        # Make API request with filters
        with st.spinner("Fetching data..."):
            response = requests.get(f"{API_BASE_URL}/data", params=params)
            
        if response.status_code == 200:
            data = response.json()
            
            if data:
                # Convert to DataFrame
                df = pd.DataFrame(data)
                
                # Convert date strings to datetime
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'])
                
                if not df.empty:
                    # Add readable names
                    if region_id_to_name:
                        df['region_name'] = df['region_id'].map(region_id_to_name)
                    else:
                        df['region_name'] = df['region_id']
                        
                    if commodity_id_to_name:
                        df['commodity_name'] = df['commodity_id'].map(commodity_id_to_name)
                    else:
                        df['commodity_name'] = df['commodity_id']
                        
                    df['created_by_name'] = df['created_by']  # Assuming created_by is already a name
                    
                    # Display data
                    st.subheader(f"Price Data ({len(df)} records)")
                    
                    # Show information about data limits
                    if len(data) >= 50000:
                        st.warning("⚠️ Showing maximum 50,000 records. There might be more data available.")
                    
                    # Show summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Records", len(df))
                    with col2:
                        if 'price' in df.columns:
                            st.metric("Avg Price", f"Rp {df['price'].mean():.2f}")
                    with col3:
                        if 'price' in df.columns:
                            st.metric("Min Price", f"Rp {df['price'].min():.2f}")
                    with col4:
                        if 'price' in df.columns:
                            st.metric("Max Price", f"Rp {df['price'].max():.2f}")
                    
                    # Create line plot if plotly is available
                    if PLOTLY_AVAILABLE:
                        create_line_plot(df)
                    else:
                        st.info("Install plotly to see price trend charts: pip install plotly")
                    
                    # Display dataframe (without id columns and with readable names)
                    display_columns = ['date', 'region_name', 'commodity_name', 'price', 'created_by_name']
                    display_df = df[display_columns].copy()
                    display_df.columns = ['Date', 'Region', 'Commodity', 'Price (Rp)', 'Created By']
                    
                    st.dataframe(display_df, use_container_width=True)
                    
                    # CSV export
                    csv = display_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name=f"price_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    
                    # Store data in session state
                    st.session_state.current_data = df
                    st.session_state.data_fetched = True
                    
                else:
                    st.warning("No data found for the selected filters.")
                    st.session_state.current_data = None
                    
            else:
                st.warning("No data found for the selected filters.")
                st.session_state.current_data = None
                
        else:
            st.error(f"Error fetching data: {response.status_code}")
            st.error(response.text)
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the API server. Please make sure the backend is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def create_line_plot(df):
    """Create a line plot showing price trends by region and commodity"""
    if not PLOTLY_AVAILABLE:
        return
        
    st.subheader("📈 Price Trends")
    
    if df.empty:
        st.warning("No data available for plotting.")
        return
    
    try:
        # Create a combined category for legend
        df['region_commodity'] = df['region_name'] + ' - ' + df['commodity_name']
        
        # Sort by date
        df_sorted = df.sort_values('date')
        
        # Create the line plot
        fig = px.line(
            df_sorted,
            x='date',
            y='price',
            color='region_commodity',
            title='Price Trends by Region and Commodity',
            labels={
                'date': 'Date',
                'price': 'Price (Rp)',
                'region_commodity': 'Region - Commodity'
            },
            hover_data=['region_name', 'commodity_name', 'price']
        )
        
        # Customize the plot
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (Rp)",
            hovermode='x unified',
            height=500,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        # Update line styles for better visibility
        fig.update_traces(
            line=dict(width=2),
            marker=dict(size=4)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating plot: {str(e)}")
        st.write("Raw data for debugging:")
        st.write(df.head()) 