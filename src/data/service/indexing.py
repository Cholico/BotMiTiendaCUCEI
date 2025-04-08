# src/data/service/indexing.py

from core.constants import table_products, table_stores
from core.firebaseHelper import db
import numpy as np
import faiss
import asyncio
import core.modelSingleton as m

# Variables globales del índice
PRODUCT_INDEX = None
PRODUCT_IDS = []
PRODUCTS_DATA = {}

STORE_INDEX = None
STORE_IDS = []
STORES_DATA = {}

def get_embedding_dim():
    if m.model is None:
        raise ValueError("El modelo de embeddings no está cargado aún.")
    return m.model.get_sentence_embedding_dimension()


def refresh_faiss_index_products():
    global PRODUCT_INDEX, PRODUCT_IDS, PRODUCTS_DATA

    if m.model is None:
        raise RuntimeError("El modelo no ha sido cargado. Asegúrate de llamar a init_embedding_model primero.")

    index = faiss.IndexFlatL2(get_embedding_dim())
    product_ids = []
    embeddings = []
    products_data = {}

    try:
        products = db.collection(table_products).stream()
        for doc in products:
            product = doc.to_dict()
            product_id = doc.id
            products_data[product_id] = product

            text = f"{product['name']} {product['description']} {' '.join(product.get('category', []))} {product['store']['name']}"
            embedding = m.model.encode(text).astype(np.float32)

            embeddings.append(embedding)
            product_ids.append(product_id)

        if embeddings:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

        PRODUCT_INDEX = index
        PRODUCT_IDS = product_ids
        PRODUCTS_DATA = products_data

    except Exception as e:
        print(f"Error al refrescar el índice de productos: {e}")


def refresh_faiss_index_stores():
    global STORE_INDEX, STORE_IDS, STORES_DATA

    if m.model is None:
        raise RuntimeError("El modelo no ha sido cargado. Asegúrate de llamar a init_embedding_model primero.")

    index = faiss.IndexFlatL2(get_embedding_dim())
    store_ids = []
    embeddings = []
    stores_data = {}

    try:
        stores = db.collection(table_stores).stream()
        for doc in stores:
            store = doc.to_dict()
            store_id = doc.id
            stores_data[store_id] = store

            text = f"{store['id']} {store['name']} {store['email']} {store['description']} {store['startTime']}-{store['endTime']} {store['rating']}"
            embedding = m.model.encode(text).astype(np.float32)

            embeddings.append(embedding)
            store_ids.append(store_id)

        if embeddings:
            embeddings_array = np.array(embeddings, dtype=np.float32)
            index.add(embeddings_array)

        STORE_INDEX = index
        STORE_IDS = store_ids
        STORES_DATA = stores_data

    except Exception as e:
        print(f"Error al refrescar el índice de tiendas: {e}")


async def periodic_faiss_refresh(interval_seconds: int = 3600):
    while True:
        try:
            refresh_faiss_index_products()
            refresh_faiss_index_stores()
        except Exception as e:
            print(f"Error al refrescar índice FAISS: {e}")
        await asyncio.sleep(interval_seconds)
