import faiss
import numpy as np
from chatbot.categories import CATEGORY_SYNONYMS
import core.modelSingleton as m
import  asyncio
import data.service.indexing as indexing

# Variables globales para el índice de categorías
CATEGORY_INDEX = None
CATEGORY_LIST = []
CATEGORY_INDEX_INITIALIZED = False

# Variables globales para el índice de descripciones de productos
DEESCRIPTION_INDEX = None
DESCRIPTION_IDS = []



def generate_embedding_simple(text: str) -> np.ndarray:
    """
    Genera el embedding vectorial de un texto (categoría) usando el modelo de SentenceTransformer.
    """
    embedding = m.model.encode(text)
    return np.array(embedding, dtype=np.float32)


def build_category_faiss_index():
    """
    Construye el índice FAISS a partir de las categorías definidas en CATEGORY_SYNONYMS.
    """
    if not CATEGORY_SYNONYMS:
        return None, []

    category_names = list(CATEGORY_SYNONYMS.keys())
    category_embeddings = [generate_embedding_simple(category) for category in category_names]

    if not category_embeddings:
        return None, []

    dim = len(category_embeddings[0])
    index = faiss.IndexHNSWFlat(dim, 32)
    index.add(np.array(category_embeddings, dtype=np.float32))

    return index, category_names


def ensure_category_index_initialized():
    """
    Asegura que el índice de categorías esté construido e inicializado.
    Esta función es idempotente.
    """
    global CATEGORY_INDEX, CATEGORY_LIST, CATEGORY_INDEX_INITIALIZED
    if CATEGORY_INDEX_INITIALIZED:
        return

    CATEGORY_INDEX, CATEGORY_LIST = build_category_faiss_index()
    CATEGORY_INDEX_INITIALIZED = True

# Construir el índice de descripciones
def build_description_faiss_index():
    descriptions = []
    product_ids = []

    # Crear lista de descripciones y sus correspondientes ids de productos
    for prod_id, prod in indexing.PRODUCTS_DATA.items():
        description = prod.get("description", "")
        if description:  # Asegurarse de que la descripción no esté vacía
            descriptions.append(generate_embedding_simple(description))
            product_ids.append(prod_id)

    # Inicializar FAISS con el número de dimensiones de los embeddings
    index = faiss.IndexHNSWFlat(len(descriptions[0]), 32)
    index.add(np.array(descriptions, dtype=np.float32))

    return index, product_ids


async def refresh_description_index(interval_seconds: int = 3600):
    while True:
        try:
            global DESCRIPTION_INDEX, DESCRIPTION_IDS
            DESCRIPTION_INDEX, DESCRIPTION_IDS = build_description_faiss_index()
        except Exception as e:
            print(f"Error al refrescar índice FAISS: {e}")
        await asyncio.sleep(interval_seconds)
