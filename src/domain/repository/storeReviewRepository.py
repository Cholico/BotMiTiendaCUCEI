from fastapi import Depends
from datetime import datetime
from typing import Annotated, Optional, Any
from data.service.storeReviewService import StoreReviewService
from domain.model.storeReviewDomain import StoreReviewDomain

class StoreReviewRepository:
    def __init__(self, service: Annotated[StoreReviewService, Depends()]):
        self.service = service

    def get_all(self) -> list[StoreReviewDomain | None]:
        response = self.service.get_all()
        return [review.to_domain() for review in response]
    
    def paging_by_store_id_with_range(
        self,
        store_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> dict[str, Any]:
        response = self.service.paging_by_store_id_with_range(
            store_id,
            limit,
            cursor,
            start_date, 
            end_date
        )
        return {
            'data': [review.to_domain() for review in response['data']],
            'next_cursor': response['next_cursor']
        }
    
    def paging_by_user_id_with_range(
        self,
        user_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> list[StoreReviewDomain | None]:
        response = self.service.paging_by_user_id_with_range(
            user_id,
            limit,
            cursor,
            start_date, 
            end_date
        )
        return {
            'data': [review.to_domain() for review in response['data']],
            'next_cursor': response['next_cursor']
        }