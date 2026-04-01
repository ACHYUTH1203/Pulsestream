PulseStream Intelligence
========================

**Real-Time Crypto Market & Sentiment Radar**

PulseStream is a full-stack, AI-powered web dashboard that tracks the top 20 cryptocurrencies and provides real-time market sentiment analysis. It leverages the CoinGecko API for live market data and utilizes Llama 3.1 (via Groq) to scrape, summarize, and analyze the sentiment of the latest cryptocurrency news headlines.

🚀 Features
-----------

*   **Liquidity Matrix (Top 20 Cryptos):** Real-time tracking of the top 20 cryptocurrencies by market cap, displaying current price, 24-hour spread, market cap, volatility, and volume-to-market-cap liquidity ratios.
    
*   **AI Market Sentiment Engine:** On-demand news analysis that scrapes recent crypto articles and uses the **Llama 3.1 8B** model to generate a concise summary and determine market sentiment (Bullish, Bearish, or Neutral).
    
*   **Automated Background Syncing:** Utilizes APScheduler to automatically synchronize market data every 24 hours to keep the database fresh without manual intervention.
    
*   **Responsive Executive UI:** A sleek, dark-themed dashboard built with Tailwind CSS that provides a high-level overview of market conditions.
    

🏗️ Architecture Overview
-------------------------

PulseStream follows a modern, decoupled architecture:

1.  **Frontend (Vanilla JS + Tailwind CSS):** A lightweight client that asynchronously requests data from the backend APIs and dynamically renders the Liquidity Matrix and News Sentiment grids.
    
2.  **Backend (FastAPI):** A high-performance Python backend that handles route management, background scheduling, and orchestrates calls to external APIs.
    
3.  **Database (PostgreSQL via SQLAlchemy):** Stores the latest snapshot of the top 20 cryptocurrencies, ensuring fast retrieval and reducing redundant calls to the CoinGecko API.
    
4.  **AI/LLM Layer (Groq + Llama 3.1):** A dedicated class that handles prompt engineering, forces JSON-formatted outputs, and processes scraped article text to return structured sentiment data.
    

### Data Flow

*   **Market Data:** The frontend requests a sync → FastAPI fetches from **CoinGecko** → Updates the **PostgreSQL** database → Serves updated data back to the frontend.
    
*   **News Sentiment:** The frontend requests news → FastAPI searches **Google News (GNews)** → Scrapes the article body using **Newspaper3k** → Passes the text to the **Groq API (Llama 3)** → Parses the structured JSON (Summary + Sentiment) → Serves it to the frontend.
    

🧩 Core Components
------------------

The codebase is modularized for scalability and maintainability:

*   **main.py**: The entry point of the application. It initializes the FastAPI app, sets up CORS, defines the API endpoints (/api/prices, /api/update-prices, /api/live-news), and manages the background scheduler for daily market updates.
    
*   **database.py**: Handles database connectivity. It configures the SQLAlchemy engine with connection pooling and sets up the session maker (SessionLocal).
    
*   **models.py**: Contains the SQLAlchemy ORM models. Defines the CryptoPrice table schema for storing coin metrics (rank, symbol, price, volume, ATH drops, etc.).
    
*   **schemas.py**: Defines the Pydantic models (e.g., CryptoPriceResponse). These are used for data validation and serialization when sending responses from the FastAPI backend to the frontend.
    
*   **services.py**: The core business logic layer.
    
    *   fetch\_and\_store\_crypto\_data(): Handles the CoinGecko API interaction, cleans up duplicate/stale records, and upserts fresh data into the database.
        
    *   get\_live\_news\_analysis(): Orchestrates the news fetching, web scraping, and LLM analysis pipeline. Includes robust error handling and fallbacks for failed scrapes.
        
*   **llm.py**: The AI engine. Contains the NewsAnalyzer class which initializes the Groq client. It utilizes a strict system prompt to force the Llama model to return objective summaries and categorical sentiments in a parseable JSON format.
    
*   **index.html**: The single-page frontend. It handles the UI layout, state management (loading spinners), data formatting, and dynamic DOM updates based on API responses.
    

🛠️ Tech Stack
--------------

**Backend & Tooling:**

*   [FastAPI](https://fastapi.tiangolo.com/) - Web framework
    
*   [Poetry](https://python-poetry.org/) - Dependency management & packaging
    
*   [SQLAlchemy](https://www.sqlalchemy.org/) - ORM
    
*   [Pydantic](https://www.google.com/search?q=https://docs.pydantic.dev/) - Data validation
    
*   [APScheduler](https://apscheduler.readthedocs.io/) - Background tasks
    

**AI & Data Scraping:**

*   [Groq API](https://groq.com/) - High-speed LLM inference (Llama 3.1 8B)
    
*   [GNews](https://github.com/ranahaani/GNews) - Google News searching
    

**Frontend:**

*   HTML5 / Vanilla JavaScript
    
*   [Tailwind CSS](https://tailwindcss.com/) - Styling
    

**APIs:**

*   [CoinGecko API](https://www.coingecko.com/en/api) - Cryptocurrency market data
    

⚙️ Setup & Installation
-----------------------

### Prerequisites

*   Python 3.9+
    
*   [Poetry](https://www.google.com/search?q=https://python-poetry.org/docs/#installation) installed on your system
    
*   PostgreSQL Database (Local or Cloud, e.g., Render)
    
*   Groq API Key
    

### Installation

1.  git clone https://github.com/yourusername/pulsestream.gitcd pulsestream
    
2.  poetry install
    
3.  DATABASE_URL=postgresql://user:password@localhost/dbnameGROQ\_API\_KEY=your\_groq\_api\_key\_here
    
4.  Bashpoetry run uvicorn main:app --reload_(Alternatively, you can enter the virtual environment using poetry shell and then just run uvicorn main:app --reload)_.
    
5.  **Access the Dashboard:**Open your browser and navigate to http://localhost:8000/.