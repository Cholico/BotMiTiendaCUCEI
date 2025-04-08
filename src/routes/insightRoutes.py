from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi_cache.decorator import cache
from controllers.insightController import InsightController
from core.constants import INSIGHT_ROUTES_GET_TOP_LOCATIONS_ON_MAP_CACHE_EXPIRE
from core.constants import INSIGHT_ROUTES_GET_TOP_SOLD_PRODUCTS_CACHE_EXPIRE
from core.constants import INSIGHT_ROUTES_CALCULATE_SALES_BY_DAY_OF_WEEK_CACHE_EXPIRE
from core.redisKeyBuilder import insight_routes_get_top_locations_on_map_key_builder
from core.redisKeyBuilder import insight_routes_get_top_sold_products_key_builder
from core.redisKeyBuilder import insight_routes_calculate_sales_by_day_of_week_key_builder

router = APIRouter()

@router.get('/insights/get-top-locations-on-map')
@cache(
    expire=INSIGHT_ROUTES_GET_TOP_LOCATIONS_ON_MAP_CACHE_EXPIRE, 
    key_builder=insight_routes_get_top_locations_on_map_key_builder
)
def get_top_locations_on_map(
    controller: Annotated[InsightController, Depends()],
    start_date: Annotated[Optional[datetime], Query()] = datetime.now() - timedelta(days=7),
    end_date: Annotated[Optional[datetime], Query()] = datetime.now()
):
    """Endpoint para obtener las 5 ubicaciones geográficas con más ventas
    :optional parameters: start_date, end_date
    :return un diccionario que contiene las ubicaciones geográficas con más ventas
    """
    return controller.get_top_locations_on_map(start_date, end_date)

@router.get('/insights/calculate-sales-by-day-of-week')
@cache(
    expire=INSIGHT_ROUTES_CALCULATE_SALES_BY_DAY_OF_WEEK_CACHE_EXPIRE,
    key_builder=insight_routes_calculate_sales_by_day_of_week_key_builder
)
def calculate_sales_by_day_of_week(
    controller: Annotated[InsightController, Depends()],
    store_id: Annotated[str, Query()],
    start_date: Annotated[Optional[datetime], Query()] = datetime.now() - timedelta(days=7),
    end_date: Annotated[Optional[datetime], Query()] = datetime.now()
):
    """Endpoint para calcular las ventas dado un rango de fechas
    :param store_id
    :optional parameters: start_date, end_date
    :return un diccionario que contiene las ventas dado un rango de fechas
    """
    return controller.calculate_sales_by_day_of_week(store_id, start_date, end_date)

@router.get('/insights/get-top-sold-products')
@cache(
    expire=INSIGHT_ROUTES_GET_TOP_SOLD_PRODUCTS_CACHE_EXPIRE,
    key_builder=insight_routes_get_top_sold_products_key_builder
)
def get_top_sold_products(
    controller: Annotated[InsightController, Depends()],
    start_date: Annotated[Optional[datetime], Query()] = datetime.now() - timedelta(days=7),
    end_date: Annotated[Optional[datetime], Query()] = datetime.now()
):
    """Endpoint para obtener los 10 productos más vendidos
    :optional parameters: start_date, end_date
    :return un diccionario que contiene los 10 productos más vendidos
    """
    return controller.get_top_sold_products(start_date, end_date)
