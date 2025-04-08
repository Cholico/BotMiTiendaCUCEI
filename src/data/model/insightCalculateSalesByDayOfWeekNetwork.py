from pydantic import BaseModel
from google.cloud.bigquery.table import Row
from datetime import date
from domain.model.insightCalculateSalesByDayOfWeekDomain import InsightCalculateSalesByDayOfWeekDomain

class InsightCalculateSalesByDayOfWeekNetwork(BaseModel):
    day_date: date
    daily_order_count: int
    daily_product_count: int
    daily_revenue: float

    @staticmethod
    def from_bq_row(row: Row) -> 'InsightCalculateSalesByDayOfWeekNetwork':
        return InsightCalculateSalesByDayOfWeekNetwork(
            day_date = row['day_date'],
            daily_order_count = row['daily_order_count'],
            daily_product_count = row['daily_product_count'],
            daily_revenue = row['daily_revenue']
        )
    
    def to_domain(self) -> InsightCalculateSalesByDayOfWeekDomain:
        return InsightCalculateSalesByDayOfWeekDomain(
            day_date = self.day_date,
            daily_order_count = self.daily_order_count,
            daily_product_count = self.daily_product_count,
            daily_revenue = self.daily_revenue
        )