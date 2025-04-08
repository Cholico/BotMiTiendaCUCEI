from fastapi import APIRouter
from data.service.recommenderService import get_similar_product_recommendations, get_similar_store_recommendations

router = APIRouter()

@router.get("/products/{product_id}/similar")
def similar_products(product_id: str):
    return get_similar_product_recommendations(product_id)


@router.get("/stores/{store_id}/similar")
def similar_stores(store_id):
    return get_similar_store_recommendations(store_id)