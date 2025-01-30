import streamlit as st
import requests
import yfinance as yf

st.title("Crypto AI Dashboard")

def get_news():
    url = "https://newsapi.org/v2/everything?q=crypto&apiKey=YOUR_NEWSAPI_KEY"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    return [f"📰 {a['title']} - {a['source']['name']}" for a in articles[:5]]

st.subheader("Последние новости")
st.write("\n".join(get_news()))

btc = yf.Ticker("BTC-USD")
btc_df = btc.history(period="1mo")
st.subheader("📊 Цена Биткоина (1 месяц)")
st.line_chart(btc_df["Close"])
