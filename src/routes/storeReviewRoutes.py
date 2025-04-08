from fastapi import APIRouter, Depends, Query
from datetime import datetime
from typing import Annotated, Optional
from fastapi_cache.decorator import cache
from controllers.storeReviewController import StoreReviewController
from core.constants import STORE_REVIEW_ROUTES_GET_ALL_CACHE_EXPIRE
from core.constants import STORE_REVIEW_ROUTES_PAGING_BY_STORE_ID_WITH_RANGE_CACHE_EXPIRE
from core.constants import STORE_REVIEW_ROUTES_PAGING_BY_USER_ID_WITH_RANGE_CACHE_EXPIRE
from core.redisKeyBuilder import store_review_routes_get_all_key_builder
from core.redisKeyBuilder import store_review_routes_paging_by_store_id_with_range_key_builder
from core.redisKeyBuilder import store_review_routes_paging_by_user_id_with_range_key_builder

router = APIRouter()

@router.get('/store-reviews')
@cache(
    expire=STORE_REVIEW_ROUTES_GET_ALL_CACHE_EXPIRE,
    key_builder=store_review_routes_get_all_key_builder
)
def get_all(controller: Annotated[StoreReviewController, Depends()]):
    """Devuelve todas las reviews analizadas"""
    return controller.get_all()

@router.get('/store-reviews/store/{store_id}')
@cache(
    expire=STORE_REVIEW_ROUTES_PAGING_BY_STORE_ID_WITH_RANGE_CACHE_EXPIRE,
    key_builder=store_review_routes_paging_by_store_id_with_range_key_builder
)
def paging_by_store_id_with_range(
    store_id: str,
    controller: Annotated[StoreReviewController, Depends()],
    limit: Annotated[int, Query()] = 10,
    next_cursor: Annotated[Optional[str], Query()] = None,
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por store_id
    :param: store_id, limit
    :optional parameers: next_cursor, start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al store_id proporcionado y el cursor para la paginación
    """
    return controller.paging_by_store_id_with_range(store_id, limit, next_cursor, start_date, end_date)

@router.get('/store-reviews/user/{user_id}')
@cache(
    expire=STORE_REVIEW_ROUTES_PAGING_BY_USER_ID_WITH_RANGE_CACHE_EXPIRE,
    key_builder=store_review_routes_paging_by_user_id_with_range_key_builder
)
def paging_by_user_id_with_range(
    user_id: str, 
    controller: Annotated[StoreReviewController, Depends()],
    limit: Annotated[int, Query()] = 10,
    next_cursor: Annotated[Optional[str], Query()] = None,
    start_date: Annotated[Optional[datetime], Query()] = None,
    end_date: Annotated[Optional[datetime], Query()] = None
):
    """Endpoint para filtrar datos por user_id
    :param: user_id, limit
    :optional parameers: next_cursor start_date, end_date
    :return un diccionario que contiene el comentario analizado de acuerdo al user_id proporcionado y el cursor para la paginación
    """
    return controller.paging_by_user_id_with_range(user_id, limit, next_cursor, start_date, end_date)
