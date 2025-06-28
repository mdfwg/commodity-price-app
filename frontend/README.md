# Commodity Price App - Frontend

A Streamlit-based web application for managing commodity price data with authentication and CRUD operations.

## Features

- 🔐 **Authentication**: Sign up and login using Supabase Auth
- 📊 **Dashboard**: View price data with filters and export to CSV
- 📝 **Add/Update Prices**: Add new price entries or update existing ones
- 🎨 **Modern UI**: Clean and responsive interface

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**:
   Create a `.env` file in the frontend directory with:
   ```
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

3. **Start Backend**:
   Make sure your FastAPI backend is running on `http://localhost:8000`

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Pages

### 1. Authentication Page
- Login with existing credentials
- Sign up for new account
- Email verification required for new accounts

### 2. Dashboard Page
- View price data in a table format
- Filter by date range, region, and commodity
- Export data to CSV
- Summary statistics (total records, average price, etc.)

### 3. Add/Update Prices Page
- Add new price entries with form validation
- Update existing price entries
- Select from predefined regions and commodities

## API Endpoints Used

- `GET /data` - Fetch price data with filters
- `POST /data` - Add new price entry
- `PUT /data/{price_id}` - Update existing price entry

## File Structure

```
frontend/
├── app.py              # Main application file
├── auth_page.py        # Authentication page
├── dashboard_page.py   # Dashboard page
├── price_form_page.py  # Add/Update prices page
├── requirements.txt    # Python dependencies
└── README.md          # This file
``` 