import streamlit as st
import yfinance as yf
import pandas as pd

# Define your stocks
stocks = {
    "Tata Steel": "TATASTEEL.NS",
    "Tata Motors": "TATAMOTORS.NS",
    "Reliance": "RELIANCE.NS",
    "Garuda": None,  # mock or skip
    "Vishal Mega Mart": None  # mock or skip
}

st.title("📈 Custom Stock Market Dashboard")

# Select stock
stock_name = st.selectbox("Choose a stock", list(stocks.keys()))
ticker_symbol = stocks[stock_name]

if ticker_symbol:
    data = yf.download(ticker_symbol, period="6mo", interval="1d")
    st.subheader(f"{stock_name} - Last 6 Months")
    st.line_chart(data['Close'])
else:
    st.warning(f"{stock_name} is not available in live stock APIs.")
