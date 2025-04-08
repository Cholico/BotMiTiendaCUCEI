from data.model.productReviewNetwork import ProductReviewNetwork
from datetime import datetime, timezone
from typing import Optional, Any

class ProductReviewService:
    def __init__(self):
        pass

    def get_all(self) -> list[ProductReviewNetwork | None]:
        product_reviews = ProductReviewNetwork.collection.fetch()
        return list(product_reviews)
    
    def paging_by_product_id_with_range(
        self,
        product_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict[str, Any]:
        query = ProductReviewNetwork.collection.filter(product_id=product_id)
        query = query.order('created_at')
        if cursor:
            query = ProductReviewNetwork.collection.cursor(cursor)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '<=', end_date)
        product_reviews_response = query.fetch(limit)
        product_reviews_list = list(product_reviews_response)
        next_cursor = product_reviews_response.cursor if len(product_reviews_list) == limit else None
        return {
            'data': product_reviews_list,
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
        query = ProductReviewNetwork.collection.filter(user_id=user_id)
        query = query.order('created_at')
        if cursor:
            query = ProductReviewNetwork.collection.cursor(cursor)
        if start_date:
            start_date = start_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '>=', start_date)
        if end_date:
            end_date = end_date.replace(tzinfo=timezone.utc)
            query = query.filter('created_at', '<=', end_date)
        product_reviews_response = query.fetch(limit)
        product_reviews_list = list(product_reviews_response)
        next_cursor = product_reviews_response.cursor if len(product_reviews_list) == limit else None
        return {
            'data': product_reviews_list,
            'next_cursor': next_cursor
        }