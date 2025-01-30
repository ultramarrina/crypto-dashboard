def analyze_news(news_title, news_description):
    prompt = f"""
    Based on the following news, provide a very short financial market insight.
    
    News Title: {news_title}
    News Description: {news_description}

    Your response should be extremely concise (max 3 sentences), clear, and investment-focused.
    Example outputs:
    - "Crypto market may rise."
    - "Stock prices of tech companies could decline."
    - "Bitcoin could experience short-term volatility."
    
    Now generate a similar short insight for this news:
    """

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[{"role": "system", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI analysis unavailable: {e}"
