from fastapi import Depends
from typing import Optional, Annotated, Any
from datetime import datetime
from core.preProcessing import cleaning_review
from core.sentimentAnalyzer import feeling_review
from domain.repository.productReviewRepository import ProductReviewRepository

class ProductReviewController:
    def __init__(self, repository: Annotated[ProductReviewRepository, Depends()]):
        self.repository = repository

    def get_all(self):
        """Devuelve todas las reviews analizadas"""
        reviews = self.repository.get_all()
        cleaned_reviews = [cleaning_review(review) for review in reviews]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return analyzed_reviews
    
    def paging_by_product_id_with_range(
        self,
        product_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> dict[str, Any]:
        """Endpoint para filtrar datos por product_id
        :param: product_id, limit
        :optional parameers: cursor, start_date, end_date
        :return un diccionario que contiene los comentarios analizados de acuerdo al product_id proporcionado y el cursor para la paginación
        """
        reviews = self.repository.paging_by_product_id_with_range(product_id, limit, cursor, start_date, end_date)
        cleaned_reviews = [cleaning_review(review) for review in reviews['data']]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return {
            "query_id": product_id, 
            "reviews": analyzed_reviews,
            "pagination": {
                "next_cursor": reviews['next_cursor']
            }
        }
    
    def paging_by_user_id_with_range(
        self, 
        user_id: str,
        limit: int,
        cursor: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ):
        """Endpoint para filtrar datos por user_id
        :param: user_id, limit
        :optional parameers: cursor, start_date, end_date
        :return un diccionario que contiene el comentario analizado de acuerdo al user_id proporcionado y el cursor para la paginación
        """
        reviews = self.repository.paging_by_user_id_with_range(user_id, limit, cursor, start_date, end_date)
        cleaned_reviews = [cleaning_review(review) for review in reviews['data']]
        analyzed_reviews = [feeling_review(review) for review in cleaned_reviews]
        return {
            "query_id": user_id, 
            "reviews": analyzed_reviews,
            "pagination": {
                "next_cursor": reviews['next_cursor']
            }
        }