import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Alpha Vantage API configuration
API_KEY = "YOUR_ALPHA_VANTAGE_API_KEY"
BASE_URL = "https://www.alphavantage.co/query"

# Stock symbol mapping
stocks = {
    "Tata Motors": "TATAMOTORS.NS",
    "Tata Steel": "TATASTEEL.NS",
    "Reliance": "RELIANCE.NS",
    "Garuda (mock)": None,
    "Vishal Mega Mart (mock)": None
}

def fetch_stock_data(symbol):
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    try:
        timeseries = data["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(timeseries, orient="index", dtype=float)
        df = df.rename(columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. adjusted close": "Adj Close",
            "6. volume": "Volume"
        })
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        return df
    except KeyError:
        return None

# Streamlit UI
st.set_page_config(page_title="📊 Stock Market Dashboard")
st.title("📈 Custom Stock Market Dashboard (Alpha Vantage)")

stock_choice = st.selectbox("Select a Stock", list(stocks.keys()))
symbol = stocks[stock_choice]

if symbol:
    data = fetch_stock_data(symbol)
    if data is not None:
        st.subheader(f"{stock_choice} - Daily Adjusted Close")
        st.line_chart(data['Adj Close'])
        st.subheader("Recent Data")
        st.dataframe(data.tail(10))
    else:
        st.error("Failed to fetch data from Alpha Vantage. You may have hit the API limit.")
else:
    st.warning(f"{stock_choice} is not available via Alpha Vantage. Showing mock data.")
    mock_data = pd.DataFrame({
        "Date": pd.date_range(end=datetime.today(), periods=10),
        "Price": [100 + i * 2 for i in range(10)]
    })
    mock_data.set_index("Date", inplace=True)
    st.line_chart(mock_data["Price"])
    st.dataframe(mock_data)

