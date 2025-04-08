import core.modelSingleton as m
import faiss
import re
import random
import numpy as np
import data.service.questionsEmbeddingsService as questionsEmbeddings
from data.service.featuresIndexingService import generate_embedding_simple
from chatbot.responses import recommendation_confused_messages

class RecommenderQueryPriocessor:
    def __init__(self, query, product_ids: list, store_ids: list, products_data: dict, store_data: dict):
        self.query = query
        self.__STORE_RECOMMENDER_QUESTIONS = questionsEmbeddings.STORE_RECOMMENDER_QUESTIONS
        self.__PRODUCT_RECOMMENDER_QUESTIONS = questionsEmbeddings.PRODUCT_RECOMMENDER_QUESTIONS

        self.__PRODUCT_IDS = product_ids
        self.__STORE_IDS = store_ids

        self.__PRODUCTS_DATA = products_data
        self.__STORES_DATA = store_data

    @staticmethod
    def __choose(quantity: int, ids: list) -> list:
        if len(ids) < quantity:
            return []
        else:
            return random.sample(ids, quantity)

    @staticmethod
    def __check_quantity_limits(quantity: int, tipo: str) -> dict | None:
        if quantity > 1000 or quantity < 0:
            return {"type": "message", "message": f"¿Que {quantity}? Jajajajaja... 😆"}
        elif quantity > 100:
            return {"type": "message", "message": f"¿Quieres {quantity} {tipo}? Me parece demasiado."}
        elif quantity > 50:
            return {"type": "message", "message": "No hay joven 🤓"}
        elif quantity > 20 and tipo == "productos":
            return {"type": "message", "message": f"¿{quantity}? ¿Estás armando un buffet o qué? 😂"}
        elif quantity > 10:
            return {"type": "message", "message": f"Ala {quantity} ¿Deseas que te arme una seccion amarilla o un menú? 📚"}
        elif quantity == 0:
            return {"type": "message", "message": "¿Recomendarte cero cosas? Filosófico 🧠"}
        elif quantity < 0:
            return {"type": "message", "message": "¿Cosas negativas? Aún no vendo arrepentimientos 🌀"}

        # Si es válido, devolvemos None para que el flujo siga
        return None


    @staticmethod
    def __extract_quantity_from_question(question: str) -> int | None:
        """
        Extrae un número desde una pregunta si hay una cantidad mencionada.
        Devuelve el número como int o None si no se encuentra.
        """
        match = re.search(r"\b(\d+)\b", question)
        if match:
            return int(match.group(1))
        return None


    def __get_recommendation_type(self, threshold: float = 0.60) -> str:
        """
        Clasifica si una pregunta es sobre recomendación de tienda o de producto.

        Args:
            threshold (float): Umbral de similitud mínima.

        Returns:
            str: 'store', 'product' o 'unknown'
        """
        embedding = generate_embedding_simple(self.query)

        # Buscar la pregunta más similar en STORE_RECOMMENDER_QUESTIONS
        store_index = faiss.IndexFlatIP(m.model.get_sentence_embedding_dimension())
        store_index.add(self.__STORE_RECOMMENDER_QUESTIONS)
        _, store_sim = store_index.search(np.array([embedding]), 1)

        # Buscar la pregunta más similar en PRODUCT_RECOMMENDER_QUESTIONS
        product_index = faiss.IndexFlatIP(m.model.get_sentence_embedding_dimension())
        product_index.add(self.__PRODUCT_RECOMMENDER_QUESTIONS)
        _, product_sim = product_index.search(np.array([embedding]), 1)

        # Obtener los valores de similitud
        store_score = float(store_sim[0][0])
        product_score = float(product_sim[0][0])

        # Comparar
        if max(store_score, product_score) < threshold:
            return "unknown"
        return "store" if store_score > product_score else "product"

    def find_recommendations(self):
        recommendation_type = self.__get_recommendation_type()
        quantity = self.__extract_quantity_from_question(self.query)
        if not quantity:
            quantity = 1  # Por defecto, recomienda uno

        if recommendation_type == "product":
            # Verificar límites
            check = self.__check_quantity_limits(quantity, "productos")
            if check: return check

            recommendation = self.__choose(quantity, self.__PRODUCT_IDS)
            if recommendation:
                productos = [self.__PRODUCTS_DATA[pid] for pid in recommendation if pid in self.__PRODUCTS_DATA]
                return {
                    "type": "product",
                    "data": productos
                }
            else:
                return {
                    "type": "message",
                    "message": "Intenté buscar productos para ti, pero no encontré nada 😢. Quizás intenta con otra pregunta."
                }

        elif recommendation_type == "store":
            # Verificar límites
            check = self.__check_quantity_limits(quantity, "tiendas")
            if check: return check

            recommendation = self.__choose(quantity, self.__STORE_IDS)
            if recommendation:
                tiendas = [self.__STORES_DATA[sid] for sid in recommendation if sid in self.__STORES_DATA]
                return {
                    "type": "store",
                    "data": tiendas
                }
            else:
                return {
                    "type": "message",
                    "message": "Busqué y busqué, pero no encontré ninguna tienda para recomendarte 🫤. Intenta preguntarme de otra forma."
                }

        else:
            return {
                "type": "message",
                "message": random.choice(recommendation_confused_messages)
            }
