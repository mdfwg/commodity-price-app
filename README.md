# 🏪 Commodity Price Management System

A comprehensive web application for managing and analyzing commodity price data across Indonesia. Built with FastAPI backend and Streamlit frontend, featuring user authentication, data visualization, and CRUD operations.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Database Setup](#-database-setup)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔐 Authentication System
- **User Registration**: Sign up with email and password
- **User Login**: Secure authentication with Supabase Auth
- **Automatic Profile Creation**: Users are automatically added to `public.users` table
- **Session Management**: Persistent login sessions
- **Role-based Access**: Support for user and admin roles

### 📊 Dashboard & Data Management
- **Interactive Dashboard**: Real-time price data visualization
- **Multi-Selection Filters**: Select multiple regions and commodities
- **Date Range Filtering**: Filter data by custom date ranges
- **Price Trend Charts**: Interactive line plots showing price trends
- **Data Export**: Download filtered data as CSV files
- **Summary Statistics**: Total records, average, min, and max prices

### 📝 Data Operations
- **Add New Prices**: Simple form to add new price entries
- **Update Prices**: Modify existing price records
- **Data Validation**: Form validation and error handling
- **Bulk Operations**: Support for multiple data entries

### 🗺️ Geographic Coverage
- **34 Indonesian Provinces**: Complete coverage of all Indonesian regions
- **13 Commodity Types**: Essential food commodities including:
  - Rice (Medium & Premium)
  - Cooking Oil (Bulk & Packaged)
  - Meat (Chicken & Beef)
  - Vegetables (Onions, Chili)
  - Basic Staples (Sugar, Eggs, Flour)

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **Supabase**: Backend-as-a-Service for database and authentication
- **PostgreSQL**: Primary database (hosted on Supabase)
- **Pydantic**: Data validation and serialization

### Frontend
- **Streamlit**: Rapid web app development framework
- **Plotly**: Interactive data visualization
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP library for API communication

### Infrastructure
- **Supabase Auth**: User authentication and management
- **Row Level Security (RLS)**: Database-level security policies
- **Environment Variables**: Secure configuration management

## 📁 Project Structure
```
commodity-price-app/
├── backend/ # FastAPI backend
│ ├── main.py # Main API endpoints
│ ├── models.py # Pydantic data models
│ ├── supabase_client.py # Supabase connection
│ └── id_mapping.py # Region/commodity ID mappings
├── frontend/ # Streamlit frontend
│ ├── app.py # Main Streamlit application
│ ├── auth_page.py # Authentication page
│ ├── dashboard_page.py # Dashboard with data visualization
│ ├── price_form_page.py # Add/Update price forms
│ └── requirements.txt # Frontend dependencies
├── data_prep/ # Data preparation scripts
├── requirements.txt # Backend dependencies
└── README.md # This file
```

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account and project
- PostgreSQL database (provided by Supabase)
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd commodity-price-app
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### 3. Install Dependencies
```bash
# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
pip install -r requirements.txt
cd ..
```

### 4. Environment Configuration
Create `.env` files in both `backend/` and `frontend/` directories:

**Backend `.env**:**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

**Frontend `.env**:**
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
```

## 🗄️ Database Setup

### 1. Supabase Project Setup
1. Create a new Supabase project
2. Get your project URL and API keys
3. Set up the database tables

### 2. Database Tables
Run the following SQL in your Supabase SQL Editor:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create prices table
CREATE TABLE IF NOT EXISTS public.prices (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    region_id UUID NOT NULL,
    commodity_id UUID NOT NULL,
    date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    created_by TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.prices ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
CREATE POLICY "Allow insert for authenticated users" ON public.users
    FOR INSERT WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Allow all operations on prices" ON public.prices
    FOR ALL USING (true);
```

## 📖 Usage Guide

### Starting the Application

1. **Start the Backend Server**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend Application**
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### User Authentication

#### Sign Up Process
1. Navigate to the "Sign Up" tab
2. Enter your email and password
3. Confirm your password
4. Click "Sign Up"
5. Check your email for verification
6. Your profile is automatically created in the database

#### Login Process
1. Navigate to the "Login" tab
2. Enter your email and password
3. Click "Login"
4. You'll be redirected to the dashboard

### Dashboard Features

#### Data Filtering
- **Date Range**: Select start and end dates to filter data
- **Regions**: Multi-select from 34 Indonesian provinces
- **Commodities**: Multi-select from 13 commodity types
- **Real-time Updates**: Data updates automatically when filters change

#### Data Visualization
- **Price Trends Chart**: Interactive line plot showing price trends
- **Summary Statistics**: Total records, average, minimum, and maximum prices
- **Data Table**: Sortable table with all price data
- **CSV Export**: Download filtered data for external analysis

#### Chart Features
- **Multiple Lines**: Each region-commodity combination has its own line
- **Interactive Hover**: Hover over points to see detailed information
- **Legend**: Color-coded legend for easy identification
- **Zoom & Pan**: Interactive chart controls

### Data Management

#### Adding New Prices
1. Navigate to "Add/Update Prices" page
2. Select "Add New Price" tab
3. Fill in the form:
   - **Region**: Select from dropdown
   - **Commodity**: Select from dropdown
   - **Date**: Choose date using date picker
   - **Price**: Enter price in Indonesian Rupiah
   - **Created By**: Your email (auto-filled)
4. Click "Add Price Entry"

#### Updating Prices
1. Navigate to "Add/Update Prices" page
2. Select "Update Price" tab
3. Choose an entry from the dropdown
4. Modify the desired fields
5. Click "Update Price Entry"

## 🔌 API Documentation

### Endpoints

#### GET `/`
- **Description**: Health check endpoint
- **Response**: `{"message": "Food Price API is running 🚀"}`

#### GET `/data`
- **Description**: Retrieve price data with filters
- **Parameters**:
  - `start_date` (optional): Start date for filtering
  - `end_date` (optional): End date for filtering
  - `regions` (optional): List of regions to filter by
  - `commodities` (optional): List of commodities to filter by
  - `limit` (optional): Maximum number of records (default: 10000)
- **Response**: Array of price data objects

#### GET `/data/count`
- **Description**: Get total count of records matching filters
- **Parameters**: Same as `/data` endpoint
- **Response**: `{"total_count": number}`

#### POST `/data`
- **Description**: Add new price entry
- **Body**: PriceData object
- **Response**: Success status and created data

#### PUT `/data/{price_id}`
- **Description**: Update existing price entry
- **Parameters**: `price_id` - UUID of the price entry
- **Body**: PriceUpdate object
- **Response**: Success status and updated data

#### DELETE `/data/{price_id}`
- **Description**: Delete price entry
- **Parameters**: `price_id` - UUID of the price entry
- **Response**: Success status and deleted data

### Data Models

#### PriceData
```json
{
  "region": "string",
  "commodity": "string",
  "date": "YYYY-MM-DD",
  "price": 0.0,
  "created_by": "string"
}
```

#### PriceUpdate
```json
{
  "region": "string (optional)",
  "commodity": "string (optional)",
  "date": "YYYY-MM-DD (optional)",
  "price": 0.0 (optional),
  "created_by": "string (optional)"
}
```

## 🎯 Supported Regions

The application supports all 34 Indonesian provinces:
- Aceh, Bali, Banten, Bengkulu
- DI Yogyakarta, DKI Jakarta
- Gorontalo, Jambi
- Jawa Barat, Jawa Tengah, Jawa Timur
- Kalimantan Barat, Kalimantan Selatan, Kalimantan Tengah, Kalimantan Timur, Kalimantan Utara
- Kepulauan Bangka Belitung, Kepulauan Riau
- Lampung, Maluku, Maluku Utara
- Nusa Tenggara Barat, Nusa Tenggara Timur
- Papua, Papua Barat
- Riau
- Sulawesi Barat, Sulawesi Selatan, Sulawesi Tengah, Sulawesi Tenggara, Sulawesi Utara
- Sumatera Barat, Sumatera Selatan, Sumatera Utara

## 🍎 Supported Commodities

The application tracks 13 essential food commodities:
- Bawang Merah (Red Onion)
- Bawang Putih Bonggol (Garlic)
- Beras Medium (Medium Rice)
- Beras Premium (Premium Rice)
- Cabai Merah Keriting (Curly Red Chili)
- Cabai Rawit Merah (Red Bird's Eye Chili)
- Daging Ayam Ras (Chicken Meat)
- Daging Sapi Murni (Beef)
- Gula Konsumsi (Consumption Sugar)
- Minyak Goreng Curah (Bulk Cooking Oil)
- Minyak Goreng Kemasan Sederhana (Simple Packaged Cooking Oil)
- Telur Ayam Ras (Chicken Eggs)
- Tepung Terigu (Curah) (Bulk Wheat Flour)

## 🔧 Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Ensure Supabase URL and keys are correct
   - Check if email verification is completed
   - Verify RLS policies are properly configured

2. **Data Loading Issues**
   - Check if backend server is running
   - Verify database connection
   - Ensure proper data format in database

3. **Chart Display Issues**
   - Install plotly: `pip install plotly`
   - Check if data contains valid date and price values

### Performance Tips

1. **Large Datasets**: Use date filters to limit data size
2. **Multiple Selections**: Limit the number of selected regions/commodities
3. **Regular Updates**: Keep the application and dependencies updated

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

**Built with ❤️ for Indonesian commodity price management**