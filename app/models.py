from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class CryptoPrice(Base):
    __tablename__ = "crypto_prices"

    id = Column(Integer, primary_key=True, index=True)
    rank = Column(Integer)
    name = Column(String, index=True)
    symbol = Column(String, index=True)
    image_url = Column(String)  
    price_usd = Column(Float)
    change_24h = Column(Float)
    market_cap = Column(Float)
    total_volume = Column(Float) 
    last_updated = Column(DateTime, default=datetime.utcnow)