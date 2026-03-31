from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CryptoPriceResponse(BaseModel):
    rank: int
    name: str
    symbol: str
    image_url: Optional[str]
    price_usd: float
    change_24h: float
    market_cap: float
    total_volume: float
    high_24h: Optional[float] = None
    low_24h: Optional[float] = None
    ath_change_percentage: Optional[float] = None
    last_updated: datetime

    class Config:
        from_attributes = True