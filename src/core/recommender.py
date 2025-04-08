import data.service.indexing as indexing
import numpy as np
from core.constants import EMBEDDINGS_MODEL, MAX_DISTANCE
from sentence_transformers import SentenceTransformer


model = SentenceTransformer(EMBEDDINGS_MODEL)

def generate_embedding_product(product):
    text = f"{product['name']} {product['description']} {' '.join(product.get('category', []))} {product['store']['name']}"
    embedding = model.encode(text).astype(np.float32)
    return embedding

def generate_embedding_store(store):
    text = f"{store['name']} {store['description']} {store['rating']} {store['totalReviews']} {store['totalRating']}"
    embedding = model.encode(text).astype(np.float32)
    return embedding

def get_similar_products(product_id: str, top_k: int = 10) -> list:
    PRODUCT_DATA = indexing.PRODUCTS_DATA
    PRODUCT_INDEX = indexing.PRODUCT_INDEX
    PRODUCT_IDS = indexing.PRODUCT_IDS

    if product_id not in PRODUCT_DATA:
        return []

    product = PRODUCT_DATA[product_id]
    query_emb = generate_embedding_product(product).reshape(1, -1)

    scores, indices = PRODUCT_INDEX.search(query_emb, top_k + 10)  # pedimos más para filtrar después

    # Filtrar por similitud (distancia menor a MAX_DISTANCE)
    candidates = [
        (PRODUCT_IDS[i], score)
        for i, score in zip(indices[0], scores[0])
        if PRODUCT_IDS[i] != product_id and score < MAX_DISTANCE
    ]

    # Ordenar por score ascendente y limitar a los mejores 5
    candidates.sort(key=lambda x: x[1])
    similar_ids = [pid for pid, _ in candidates[:5]]

    return similar_ids


def get_similar_stores(product_id: str, top_k: int = 10) -> list:
    STORE_DATA = indexing.STORES_DATA
    STORE_INDEX = indexing.STORE_INDEX
    STORE_IDS = indexing.STORE_IDS

    if product_id not in STORE_DATA:
        return []

    store = STORE_DATA[product_id]
    query_emb = generate_embedding_store(store).reshape(1, -1)

    scores, indices = STORE_INDEX.search(query_emb, top_k + 10)  # pedimos más para filtrar después

    # Filtrar por similitud (distancia menor a MAX_DISTANCE)
    candidates = [
        (STORE_IDS[i], score)
        for i, score in zip(indices[0], scores[0])
        if STORE_IDS[i] != product_id and score < MAX_DISTANCE
    ]

    # Ordenar por score ascendente y limitar a los mejores 5
    candidates.sort(key=lambda x: x[1])
    similar_ids = [pid for pid, _ in candidates[:5]]

    return similar_ids