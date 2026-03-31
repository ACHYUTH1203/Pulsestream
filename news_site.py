import streamlit as st
import requests

st.set_page_config(page_title="PulseStream | Live News Radar", layout="wide", page_icon="🚀")

st.title("PulseStream: Real-Time Crypto Intelligence")
st.markdown("### AI-Powered Sentiment Analysis")
st.divider()

if st.button("Refresh & Analyze Latest 24H News"):
    with st.spinner("scraping and analyzing market news ..."):
        try:
            # Connects to your FastAPI Backend
            response = requests.get("http://localhost:8000/api/live-news")
            
            if response.status_code == 200:
                news_data = response.json()
                
                if not news_data:
                    st.warning("No news found in the last 24 hours.")
                
                for news in news_data:
                    with st.container(border=True):
                        # Sentiment Badge
                        sentiment = news['sentiment']
                        emoji = "🚀" if sentiment == "Bullish" else "📉" if sentiment == "Bearish" else "⚖️"
                        
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            st.metric("Sentiment", f"{emoji} {sentiment}")

                        
                        with col2:
                            st.subheader(news['title'])
                            st.write(f"**AI Summary:** {news['summary']}")
                            st.caption(f"Source: {news['publisher']} | {news['published_at']}")
                            st.link_button("Read Full Article", news['url'])
            else:
                st.error("Backend server is running but returned an error.")
        except Exception as e:
            st.error(f"Could not connect to PulseStream Backend. Is it running at localhost:8000? Error: {e}")
else:
    st.info("Click the button above to trigger the real-time News Engine.")