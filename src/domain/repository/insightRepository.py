from typing import Annotated
from datetime import datetime
from fastapi.params import Depends
from data.service.insightService import InsightService
from domain.model.insightCalculateSalesByDayOfWeekDomain import InsightCalculateSalesByDayOfWeekDomain
from domain.model.insightTopLocationDomain import InsightTopLocationDomain
from domain.model.insightTopSoldProductDomain import InsightTopSoldProductDomain

class InsightRepository:
    def __init__(self, service: Annotated[InsightService, Depends()]):
        self.service = service

    def get_top_locations_on_map(
        self,
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightTopLocationDomain]]:
        results = self.service.get_top_locations_on_map(start_date, end_date)
        return {
            'data': [result.to_domain() for result in results]
        }
    
    def calculate_sales_by_day_of_week(
        self, 
        store_id: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightCalculateSalesByDayOfWeekDomain]]:
        results = self.service.calculate_sales_by_day_of_week(store_id, start_date, end_date)
        return {
            'data': [result.to_domain() for result in results]
        }
    
    def get_top_sold_products(
        self,
        start_date: datetime, 
        end_date: datetime
    ) -> dict[str, list[InsightTopSoldProductDomain]]:
        results = self.service.get_top_sold_products(start_date, end_date)
        return {
            'data': [result.to_domain() for result in results]
        }