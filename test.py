import requests
import json

def verify_coingecko_json():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 2, # Just fetching 2 coins so it doesn't flood your terminal
        "page": 1,
        "sparkline": False
    }
    
    print("Fetching raw data from CoinGecko...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Print the raw JSON beautifully formatted
        print(json.dumps(data, indent=4))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    verify_coingecko_json()