import streamlit as st
import requests
import yfinance as yf
import openai
import os

st.title("Crypto AI Dashboard")

# API Keys
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to fetch news
def get_news():
    url = f"https://newsapi.org/v2/everything?q=crypto&language=en&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        return articles[:5]  # Return top 5 articles
    else:
        return []

# Function to analyze news impact with AI (Updated for OpenAI 1.0.0+)
def analyze_news(news_title, news_description):
    prompt = f"""
    Analyze the following news and explain how it impacts the stock and crypto markets.
    
    News Title: {news_title}
    News Description: {news_description}
    
    Your answer should be concise and provide clear insights for investors.
    """

    try:
        client = openai.OpenAI()  # New client initialization
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {e}"

# Display news
st.subheader("📰 Latest News")
news_list = get_news()

if news_list:
    for news in news_list:
        st.markdown(f"### [{news['title']}]({news['url']})")
        st.write(news["description"])
        analysis = analyze_news(news["title"], news["description"])
        st.write(f"📊 **AI Insight:** {analysis}")
        st.markdown("---")  # Separator line
else:
    st.write("⚠️ No news available. API Error!")

# Bitcoin price chart
btc = yf.Ticker("BTC-USD")
btc_df = btc.history(period="1mo")
st.subheader("📊 Bitcoin Price (1 Month)")
st.line_chart(btc_df["Close"])
