from typing import Optional

from pydantic import BaseModel


class SearchQuery(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    usage: Optional[str] = None
    price: Optional[float] = None
    city: Optional[str] = None
    body_type: Optional[str] = None
    fuel_type: Optional[str] = None