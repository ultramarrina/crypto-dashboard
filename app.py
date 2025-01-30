import streamlit as st
import yfinance as yf
import requests
import pandas as pd

st.title("Crypto AI Dashboard")

# Function to get Yahoo Finance news
def get_news():
    url = "https://query1.finance.yahoo.com/v1/finance/search?q=crypto"
    response = requests.get(url).json()
    articles = response.get("news", [])
    return [f"📰 {a['title']} - {a['publisher']}" for a in articles[:5]]

st.subheader("Latest News")
news_list = get_news()
if news_list:
    st.write("\n".join(news_list))
else:
    st.write("⚠️ No news available. Try again later.")

# Bitcoin price chart
btc = yf.Ticker("BTC-USD")
btc_df = btc.history(period="1mo")
st.subheader("📊 Bitcoin Price (1 Month)")
st.line_chart(btc_df["Close"])
