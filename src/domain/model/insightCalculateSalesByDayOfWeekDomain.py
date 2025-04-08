from pydantic import BaseModel
from datetime import date

class InsightCalculateSalesByDayOfWeekDomain(BaseModel):
    day_date: date
    daily_order_count: int
    daily_product_count: int
    daily_revenue: float