from sentence_transformers import SentenceTransformer
from core.constants import EMBEDDINGS_MODEL

model = None

def init_embedding_model():
    global model
    model = SentenceTransformer(EMBEDDINGS_MODEL)
    print("Modelo de embeddings cargado:", model.get_sentence_embedding_dimension())