import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Alpha Vantage API configuration
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"  # Replace with your actual API key
BASE_URL = "https://www.alphavantage.co/query"

# Stock symbol mapping
stocks = {
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Reliance": "RELIANCE.NS",
    "Garuda (mock)": None,
    "Vishal Mega Mart (mock)": None
}

# Function to fetch data from Alpha Vantage
def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Check for valid time series key
        if "Time Series (Daily)" not in data:
            return None

        timeseries = data["Time Series (Daily)"]
        df = pd.DataFrame(timeseries).T  # Transpose to get dates as rows
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. adjusted close": "Adj Close",
            "6. volume": "Volume"
        })

        # Convert columns to numeric
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)

        return df

    except (requests.exceptions.RequestException, ValueError) as e:
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="📊 Stock Market Dashboard")
st.title("📈 Custom Stock Market Dashboard (Alpha Vantage)")

stock_choice = st.selectbox("Select a Stock", list(stocks.keys()))
symbol = stocks[stock_choice]

if symbol:
    with st.spinner("Fetching data..."):
        data = fetch_stock_data(symbol)

    if data is not None:
        st.subheader(f"{stock_choice} - Daily Adjusted Close (Last 60 Days)")
        st.line_chart(data['Adj Close'])
        st.subheader("📄 Latest 10 Days Data")
        st.dataframe(data.tail(10))
    else:
        st.error("❌ Failed to fetch data from Alpha Vantage.\nYou may have hit the API limit or the symbol is incorrect.")
else:
    st.warning(f"⚠️ {stock_choice} is not listed. Showing mock data.")
    mock_data = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "Price": [100 + i * 2 for i in range(10)]
    })
    mock_data.set_index("Date", inplace=True)
    st.line_chart(mock_data["Price"])
    st.dataframe(mock_data)
