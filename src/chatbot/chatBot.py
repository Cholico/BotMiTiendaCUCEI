import core.modelSingleton as m
import data.service.questionsEmbeddingsService as questionsEmbeddings
import data.service.indexing as indexing
import numpy as np
import random
from chatbot.responses import no_sense_responses, greeting_responses
import unicodedata
import re
from  chatbot.productQueryProcessor import ProductQueryProcessor
from chatbot.storeQueryProcessor import StoreQueryProccesor
from chatbot.recommenderQueryProcessor import RecommenderQueryPriocessor


class ChatBot:
    def __init__(self):
        # Generar embeddings para los productos (esto ayudara al bot  a entender las preguntas)
        self.__store_embeddings_questions = questionsEmbeddings.STORE_QUESTIONS_EMBEDDINGS
        self.__product_embeddings_questions = questionsEmbeddings.PRODUCT_QUESTIONS_EMBEDDINGS
        self.__recom_embeddings_questions = questionsEmbeddings.RECOMMENDATION_QUESTIONS_EMBEDDINGS
        self.__greetings_embeddings_questions = questionsEmbeddings.GREETING_QUESTIONS_EMBEDDINGS

        # Generar su banco de memoria
        self.__PRODUCT_IDS = indexing.PRODUCT_IDS
        self.__PRODUCTS_DATA = indexing.PRODUCTS_DATA
        self.PRODUCT_INDEX = indexing.PRODUCT_INDEX

        self.__STORE_INDEX = indexing.STORE_INDEX
        self.__STORE_IDS = indexing.STORE_IDS
        self.__STORES_DATA = indexing.STORES_DATA


    # Normalizar query
    @staticmethod
    def __normalize_query(query: str) -> str:
        # Pasar a minúsculas
        query = query.lower()

        # Eliminar acentos/tildes
        query = unicodedata.normalize('NFD', query)
        query = query.encode('ascii', 'ignore').decode('utf-8')

        # Eliminar puntuación
        query = re.sub(r'[^\w\s]', '', query)

        # Quitar espacios extras
        query = re.sub(r'\s+', ' ', query).strip()

        return query

    def process_query(self, query: str) -> str | dict:
        """Clasifica la consulta como 'product', 'store', 'recommendation', 'greeting' o 'unknown'."""

        # Generar el embedding de la consulta del usuario
        query_embedding = m.model.encode([query], normalize_embeddings=True)[0]

        # Calcular similitudes con cada tipo de ejemplos
        product_similarities = np.dot(self.__product_embeddings_questions, query_embedding)
        store_similarities = np.dot(self.__store_embeddings_questions, query_embedding)
        recommen_similarities = np.dot(self.__recom_embeddings_questions, query_embedding)
        greetings_similarities = np.dot(self.__greetings_embeddings_questions, query_embedding)

        # Obtener la mejor similitud de cada categoría
        best_product_sim = max(product_similarities)
        best_store_sim = max(store_similarities)
        best_recomm_sim = max(recommen_similarities)
        best_greet_sim = max(greetings_similarities)

        # Ajustar umbral de confianza entre mss pequeqño sea, sera as exigente
        threshold = 0.3

        query = self.__normalize_query(query)

        # Clasificar según la similitud más alta
        if best_product_sim > threshold and best_product_sim > max(best_store_sim, best_recomm_sim, best_greet_sim):
            # Inicializa el query processor para productos
            queryProducts = ProductQueryProcessor(query, self.__PRODUCT_IDS, self.__PRODUCTS_DATA)
            return queryProducts.find_products()
        elif best_store_sim > threshold and best_store_sim > max(best_product_sim, best_recomm_sim, best_greet_sim):
            queryStores = StoreQueryProccesor(query, self.__STORE_INDEX, self.__STORE_IDS, self.__STORES_DATA)
            return queryStores.find_stores()
        elif best_recomm_sim > threshold and best_recomm_sim > max(best_product_sim, best_store_sim, best_greet_sim):
            queryRecommendations = RecommenderQueryPriocessor(query, self.__PRODUCT_IDS, self.__STORE_IDS, self.__PRODUCTS_DATA, self.__STORES_DATA)
            return queryRecommendations.find_recommendations()
        elif best_greet_sim > threshold and best_greet_sim > max(best_product_sim, best_store_sim, best_recomm_sim):
            return {"type": "message",
                    "message": random.choice(greeting_responses)}
        else:
            return {"type": "message",
                "message": random.choice(no_sense_responses)}

