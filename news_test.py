import json
from app.services import get_live_news_analysis
from dotenv import load_dotenv

# 1. Load environment variables for Groq API Key
load_dotenv()

def run_news_test():
    print("="*60)
    print("PULSESTREAM NEWS ENGINE: LIVE TEST SIMULATION")
    print("="*60)
    
    try:
        # 2. Trigger the live analysis (Scrape -> Truncate -> Groq)
        # This uses the 'Direct LLM' approach we discussed
        results = get_live_news_analysis()
        
        if not results:
            print("\n[!] No news found or all articles failed analysis.")
            return

        print(f"\n[SUCCESS] Analyzed {len(results)} articles.\n")

        # 3. Print the output to see what is "Visible"
        for i, news in enumerate(results, 1):
            print(f"ARTICLE #{i}")
            print(f"Title:     {news['title']}")
            print(f"Publisher: {news['publisher']}")
            print(f"Published: {news['published_at']}")
            print(f"URL:       {news['url']}")
            print("-" * 30)
            print(f"SENTIMENT: {news['sentiment']} {get_emoji(news['sentiment'])}")

            print(f"AI SUMMARY: {news['ai_summary']}")
            print("="*60)

    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")

def get_emoji(sentiment):
    if sentiment == "Bullish": return "🚀"
    if sentiment == "Bearish": return "📉"
    return "⚖️"

if __name__ == "__main__":
    run_news_test()