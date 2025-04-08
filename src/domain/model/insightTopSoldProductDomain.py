from pydantic import BaseModel
from datetime import datetime

class InsightTopSoldProductDomain(BaseModel):
    id: str
    name: str
    description: str
    image: str
    category_name: str
    store_name: str
    store_owner_id: str
    discount_percentage: float
    discount_start_date: datetime
    discount_end_date: datetime
    rating: float
    total_reviews: int
    total_quantity_sold: int
    hits_on_orders: int
    