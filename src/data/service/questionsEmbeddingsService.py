import core.modelSingleton as m
from chatbot.questions import *

EMBEDDING_DIM = m.model.get_sentence_embedding_dimension()

# Variables globales
STORE_QUESTIONS_EMBEDDINGS = None
PRODUCT_QUESTIONS_EMBEDDINGS = None
RECOMMENDATION_QUESTIONS_EMBEDDINGS = None
GREETING_QUESTIONS_EMBEDDINGS = None
OPEN_NOW_EMBEDDINGS = None
OPENING_HOURS_EMBEDDINGS = None
RANKING_STORE_EMBEDDINGS = None
DESCRIPTION_STORE_EMBEDDINGS = None

# Recommender Questions
STORE_RECOMMENDER_QUESTIONS = None
PRODUCT_RECOMMENDER_QUESTIONS = None

def generate_question_embeddings():
    global STORE_QUESTIONS_EMBEDDINGS, PRODUCT_QUESTIONS_EMBEDDINGS
    global RECOMMENDATION_QUESTIONS_EMBEDDINGS, GREETING_QUESTIONS_EMBEDDINGS
    global OPEN_NOW_EMBEDDINGS, OPENING_HOURS_EMBEDDINGS
    global RANKING_STORE_EMBEDDINGS, DESCRIPTION_STORE_EMBEDDINGS
    global STORE_RECOMMENDER_QUESTIONS, PRODUCT_RECOMMENDER_QUESTIONS

    # Genera embeddings de preguntas sobre el tipo de preguntas o entradas que el bot recibira
    STORE_QUESTIONS_EMBEDDINGS = m.model.encode(store_examples, normalize_embeddings=True)
    PRODUCT_QUESTIONS_EMBEDDINGS = m.model.encode(product_examples, normalize_embeddings=True)
    RECOMMENDATION_QUESTIONS_EMBEDDINGS = m.model.encode(recommendation_examples, normalize_embeddings=True)
    GREETING_QUESTIONS_EMBEDDINGS = m.model.encode(greeting_examples, normalize_embeddings=True)

    # Genera embeddings de preguntas sobre tiendas
    OPEN_NOW_EMBEDDINGS = m.model.encode(open_now_examples, normalize_embeddings=True)
    OPENING_HOURS_EMBEDDINGS = m.model.encode(opening_hours_examples, normalize_embeddings=True)
    RANKING_STORE_EMBEDDINGS = m.model.encode(questions_about_rankings, normalize_embeddings=True)
    DESCRIPTION_STORE_EMBEDDINGS = m.model.encode(questions_about_description, normalize_embeddings=True)

    # Genera embeddings para preguntas recomendadoras específicas (tiendas o productos)
    STORE_RECOMMENDER_QUESTIONS = m.model.encode(store_recommender_examples, normalize_embeddings=True)
    PRODUCT_RECOMMENDER_QUESTIONS = m.model.encode(product_recommender_examples, normalize_embeddings=True)
