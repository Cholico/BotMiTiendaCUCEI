import hashlib
from datetime import datetime, timedelta
from fastapi import Request, Response
from core.constants import REDIS_CACHE_PREFIX

def insight_routes_get_top_locations_on_map_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    start_date = request.query_params.get('start_date') if 'start_date' in request.query_params else datetime.now().date() - timedelta(days=7)
    end_date = request.query_params.get('end_date') if 'end_date' in request.query_params else datetime.now().date()
    raw_key = f'insight-routes:get-top-locations-on-map:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def insight_routes_calculate_sales_by_day_of_week_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    store_id = request.query_params.get('store_id')
    start_date = request.query_params.get('start_date') if 'start_date' in request.query_params else datetime.now().date() - timedelta(days=7)
    end_date = request.query_params.get('end_date') if 'end_date' in request.query_params else datetime.now().date()
    raw_key = f'insight-routes:calculate-sales-by-day-of-week:{store_id}:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def insight_routes_get_top_sold_products_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    start_date = request.query_params.get('start_date') if 'start_date' in request.query_params else datetime.now().date() - timedelta(days=7)
    end_date = request.query_params.get('end_date') if 'end_date' in request.query_params else datetime.now().date()
    raw_key = f'insight-routes:get-top-sold-products:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def product_review_routes_get_all_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    raw_key = 'product-review-routes:get-all'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def product_review_routes_paging_by_product_id_with_range_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    product_id = request.path_params.get('product_id')
    limit = request.query_params.get('limit')
    next_cursor = request.query_params.get('next_cursor')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    raw_key = f'product-review-routes:paging-by-product-id-with-range:{product_id}:{limit}:{next_cursor}:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def product_review_routes_paging_by_user_id_with_range_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    user_id = request.path_params.get('user_id')
    limit = request.query_params.get('limit')
    next_cursor = request.query_params.get('next_cursor')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    raw_key = f'product-review-routes:paging-by-user-id-with-range:{user_id}:{limit}:{next_cursor}:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def store_review_routes_get_all_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    raw_key = 'store-review-routes:get-all'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def store_review_routes_paging_by_store_id_with_range_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    store_id = request.path_params.get('store_id')
    limit = request.query_params.get('limit')
    next_cursor = request.query_params.get('next_cursor')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    raw_key = f'store-review-routes:paging-by-store-id-with-range:{store_id}:{limit}:{next_cursor}:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'

def store_review_routes_paging_by_user_id_with_range_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs
):
    user_id = request.path_params.get('user_id')
    limit = request.query_params.get('limit')
    next_cursor = request.query_params.get('next_cursor')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    raw_key = f'store-review-routes:paging-by-user-id-with-range:{user_id}:{limit}:{next_cursor}:{start_date}:{end_date}'
    hashed_key = hashlib.md5(raw_key.encode()).hexdigest() # avoid redis key length limit
    return f'{REDIS_CACHE_PREFIX}:{hashed_key}'