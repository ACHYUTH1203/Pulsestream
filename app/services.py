import os
import requests
from sqlalchemy.orm import Session
from datetime import datetime
from .models import CryptoPrice
from .llm import analyzer
from gnews import GNews
from newspaper import Article
from groq import Groq




def fetch_and_store_crypto_data(db: Session):
    """Fetches Top 20 coins from CoinGecko and upserts them to PostgreSQL."""
    
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1,
        "sparkline": False
    }
    
    print("Fetching live data from CoinGecko...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"CoinGecko API Error: {response.status_code}")
        
    data = response.json()
    print(f"Success! Fetched {len(data)} coins. Updating Render database...")
    

    existing_coins = {coin.symbol: coin for coin in db.query(CryptoPrice).all()}

    for coin in data:
        symbol = coin['symbol'].upper()
        
        fresh_data = {
            "rank": coin.get('market_cap_rank', 0),
            "name": coin.get('name', ''),
            "image_url": coin.get('image', ''),
            "price_usd": coin.get('current_price', 0.0),
            "change_24h": coin.get('price_change_percentage_24h', 0.0),
            "market_cap": coin.get('market_cap', 0.0),
            "total_volume": coin.get('total_volume', 0.0),
            "high_24h": coin.get('high_24h', 0.0),
            "low_24h": coin.get('low_24h', 0.0),
            "ath_change_percentage": coin.get('ath_change_percentage', 0.0),
            "last_updated": datetime.utcnow()
        }

        if symbol in existing_coins:

            existing_record = existing_coins[symbol]
            for key, value in fresh_data.items():
                setattr(existing_record, key, value)
        else:
   
            new_entry = CryptoPrice(symbol=symbol, **fresh_data)
            db.add(new_entry)
            
    db.commit()
    return {"message": "Market snapshot synchronized successfully."}

def get_live_news_analysis():
    """
    PRODUCTION-GRADE: Performs real-time news extraction and AI analysis.
    Includes robust fallbacks to ensure the UI never displays empty or 'None' values.
    """
    print("PulseStream News Engine: Production Analysis Mode")
    

    google_news = GNews(language='en', period='1d', max_results=6)
    items = google_news.get_news('Cryptocurrency OR Bitcoin OR Ethereum')
    
    analyzed_news = []
    
    for item in items:
        try:

            article = Article(item['url'])
            article.download()
            article.parse()
            
            raw_text = article.text[:4000] 
            
            analysis = analyzer.analyze_article(item['title'], raw_text)
            
            final_summary = analysis.get("summary")
            if not final_summary or len(str(final_summary).strip()) < 10:

                final_summary = raw_text[:250].replace('\n', ' ').strip() + "..."
            
            
            sentiment = analysis.get("sentiment")
            if not sentiment or sentiment == "None":
                sentiment = "Neutral"
                


            analyzed_news.append({
                "title": item['title'],
                "url": item['url'],
                "publisher": item['publisher']['title'],
                "published_at": item['published date'],
                "ai_summary": final_summary,
                "sentiment": sentiment,
                
            })
            
            print(f"Analysis Complete: {item['title'][:50]}...")
            
        except Exception as e:
            print(f"Skipping article {item.get('url', 'Unknown URL')}: {e}")
            continue
            
    return analyzed_news