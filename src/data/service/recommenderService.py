from domain.repository import storeRepository, productRepository
from core.recommender import get_similar_stores, get_similar_products


def get_similar_product_recommendations(product_id: str):
    original = productRepository.get_product_by_id(product_id)
    if not original:
        return {"error": "Producto no encontrado"}

    similar_ids = get_similar_products(product_id)
    similar_products = productRepository.get_products_by_ids(similar_ids)
    return similar_products



def get_similar_store_recommendations(store_id: str):
    original = storeRepository.get_store_by_id(store_id)
    if not original:
        return {"error": "Tienda no encontrada"}

    similar_ids = get_similar_stores(store_id)
    similar_stores = storeRepository.get_stores_by_ids(similar_ids)
    return similar_stores