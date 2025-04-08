from data.model.storeReviewNetwork import StoreReviewNetwork
from datetime import datetime, timezone
from typing import Optional, Any

class StoreReviewService:
    def __init__(self):
        pass

    def get_all(self) -> list[StoreReviewNetwork | None]:
        store_reviews = StoreReviewNetwork.collection.fetch()
        return list(store_reviews)

    def paging_by_store_id_with_range(
        self,
        store_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> dict[str, Any]:
        query = StoreReviewNetwork.collection.filter(store_id=store_id)
        query = query.order('created_at')
        if cursor:
            query = StoreReviewNetwork.collection.cursor(cursor)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '<=', end_date)
        store_reviews_response = query.fetch(limit)
        store_reviews_list = list(store_reviews_response)
        next_cursor = store_reviews_response.cursor if len(store_reviews_list) == limit else None
        return {
            'data': store_reviews_list,
            'next_cursor': next_cursor
        }
    
    def paging_by_user_id_with_range(
        self, 
        user_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None, 
        end_date: Optional[datetime] = None
    ) -> dict[str, Any]:
        query = StoreReviewNetwork.collection.filter(user_id=user_id)
        query = query.order('created_at')
        if cursor:
            query = StoreReviewNetwork.collection.cursor(cursor)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '<=', end_date)
        store_reviews_response = query.fetch(limit)
        store_reviews_list = list(store_reviews_response)
        next_cursor = store_reviews_response.cursor if len(store_reviews_list) == limit else None
        return {
            'data': store_reviews_list,
            'next_cursor': next_cursor
        }
        
