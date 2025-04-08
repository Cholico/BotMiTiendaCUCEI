from typing import Annotated
from datetime import datetime
from fastapi.params import Depends
from domain.model.insightCalculateSalesByDayOfWeekDomain import InsightCalculateSalesByDayOfWeekDomain
from domain.model.insightTopLocationDomain import InsightTopLocationDomain
from domain.model.insightTopSoldProductDomain import InsightTopSoldProductDomain
from domain.repository.insightRepository import InsightRepository


class InsightController:
    def __init__(self, repository: Annotated[InsightRepository, Depends()]):
        self.repository = repository

    def get_top_locations_on_map(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightTopLocationDomain]]:
        return self.repository.get_top_locations_on_map(start_date, end_date)
    
    def calculate_sales_by_day_of_week(
        self, 
        store_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightCalculateSalesByDayOfWeekDomain]]:
        return self.repository.calculate_sales_by_day_of_week(store_id, start_date, end_date)
    
    def get_top_sold_products(
        self, 
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightTopSoldProductDomain]]:
        return self.repository.get_top_sold_products(start_date, end_date)