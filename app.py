import streamlit as st
import requests
import yfinance as yf
import os

st.title("Crypto AI Dashboard")

# Load NewsAPI key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "YOUR_NEWSAPI_KEY_HERE")

def get_news():
    url = f"https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return [f"📰 {a['title']} - {a['source']['name']}" for a in articles[:5]]
    else:
        return ["⚠️ No news available. API Error!"]

st.subheader("Latest News")
news_list = get_news()
st.write("\n".join(news_list))

btc = yf.Ticker("BTC-USD")
btc_df = btc.history(period="1mo")
st.subheader("📊 Bitcoin Price (1 Month)")
st.line_chart(btc_df["Close"])
