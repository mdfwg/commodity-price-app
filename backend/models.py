from pydantic import BaseModel
from typing import Optional
from datetime import date

class PriceData(BaseModel):
    region: str
    commodity: str
    date: date
    price: float
    created_by: str

class PriceFilter(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    region_id: Optional[str] = None
    commodity_id: Optional[str] = None

class PriceUpdate(BaseModel):
    region: Optional[str] = None
    commodity: Optional[str] = None
    date: Optional["date"] = None
    price: Optional[float] = None
    created_by: Optional[str] = None