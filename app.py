import streamlit as st
import requests
import yfinance as yf
import openai
import os
import traceback

# Debugging: Show errors in Streamlit UI
try:
    st.title("Crypto AI Dashboard")
except Exception as e:
    st.error(f"❌ Error in the app: {e}")
    st.text(traceback.format_exc())

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

# Function to analyze news impact with AI (short insights)
def analyze_news(news_title, news_description):
    prompt = f"""
    Based on the following news, provide a **very short** financial market insight.
    
    News Title: {news_title}
    News Description: {news_description}

    Your response should be **max 2 sentences**, clear, and investment-focused.
    Example outputs:
    - "Crypto market may rise."
    - "Stock prices of tech companies could decline."
    - "Bitcoin could experience short-term volatility."
    
    Now generate a similar short insight for this news:
    """

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4o-mini for cost efficiency
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
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
