import os 
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from . import models, database, schemas, services
from .database import engine, get_db
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .database import SessionLocal
from .services import fetch_and_store_crypto_data



models.Base.metadata.create_all(bind=engine)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize and start the scheduler
    scheduler = BackgroundScheduler()
    # interval could be 'hours=24' or 'minutes=1' for testing
    scheduler.add_job(scheduled_market_update, 'interval', hours=24)
    scheduler.start()
    print(" PulseStream: Background Scheduler Started.")
    
    yield
    
    # Shutdown scheduler when app stops
    scheduler.shutdown()
    print(" PulseStream: Background Scheduler Stopped.")
app = FastAPI(
    title="PulseStream API", 
    lifespan=lifespan,
    description="Real-time market intel and routing data for TransFi",
    version="1.0.0"
)

# Add CORS middleware to allow your future frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
def scheduled_market_update():
    print("PulseStream: Starting scheduled daily market update...")
    db = SessionLocal()
    try:
        fetch_and_store_crypto_data(db)
        print("PulseStream: Scheduled update successful.")
    except Exception as e:
        print(f"PulseStream: Scheduled update failed: {e}")
    finally:
        db.close()




@app.post("/api/update-prices", summary="Fetch latest prices from CoinGecko and store in DB")
def update_prices(db: Session = Depends(get_db)):
    """
    Triggers a fetch from the CoinGecko API and upserts the Top 20 
    cryptocurrencies into the Render PostgreSQL database.
    """
    try:
        result = services.fetch_and_store_crypto_data(db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/prices", response_model=list[schemas.CryptoPriceResponse], summary="Get stored crypto prices")
def get_prices(db: Session = Depends(get_db)):
    """
    Retrieves the stored Top 20 cryptocurrencies from the database, 
    ordered by their market cap rank.
    """
    prices = db.query(models.CryptoPrice).order_by(models.CryptoPrice.rank).limit(20).all()
    return prices

@app.get("/api/live-news", summary="Get real-time AI analyzed news (Not stored in DB)")
async def live_news():
    """
    Calls the News Engine to scrape and analyze current crypto headlines.
    This is used by the separate News Site.
    """
    try:
        data = services.get_live_news_analysis()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # This looks for the 'frontend' folder in your project root
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "frontend", "index.html")
    
    if not os.path.exists(file_path):
        return HTMLResponse(content="<h1>Frontend file not found</h1>", status_code=404)
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()