import numpy as np
import random
import re
from datetime import datetime
from data.service.featuresIndexingService import generate_embedding_simple
import data.service.questionsEmbeddingsService as questionsEmbeddings
from chatbot.responses import stores_no_sense_response, no_open_stores_message, no_found_stores
from difflib import get_close_matches


class StoreQueryProccesor:
    def __init__(self, query: str, store_index: list, store_ids: list, stores_data: dict):
        self.query = query
        self.__STORE_INDEX = store_index
        self.__STORE_IDS = store_ids
        self.__STORES_DATA = stores_data

        # Question embeddings
        self.__OPEN_NOW_EMBEDDINGS = questionsEmbeddings.OPEN_NOW_EMBEDDINGS
        self.__OPENING_HOURS_EMBEDDINGS = questionsEmbeddings.OPENING_HOURS_EMBEDDINGS
        self.__RANKING_STORE_EMBEDDINGS = questionsEmbeddings.RANKING_STORE_EMBEDDINGS
        self.__DESCRIPTION_STORE_EMBEDDINGS = questionsEmbeddings.DESCRIPTION_STORE_EMBEDDINGS

    def __find_similar_store(self, k: int = 1) ->list[dict]:
        """
        Busca la tienda más similar a la consulta del usuario usando FAISS y embeddings.
        Retorna un listado con hasta k tiendas similares (por defecto solo la más similar).
        """

        # Generar embedding de la consulta
        embedding = generate_embedding_simple(self.query)

        # Buscar los k más cercanos en el índice FAISS
        distances, indices = self.__STORE_INDEX.search(embedding, k)

        # Obtener los datos de las tiendas encontradas
        results = []
        for idx in indices[0]:
            if idx < len(self.__STORE_IDS):
                store_id = self.__STORE_IDS[idx]
                store_data = self.__STORES_DATA.get(store_id)
                if store_data:
                    results.append(store_data)

        return results


    def __get_stores_by_rating(self) -> list[dict] | str:
        # Predeterminado: mayor a menor
        reverse = True

        if "bajo" in self.query or "peor" in self.query or "menor" in self.query:
            reverse = False

        # Tiendas con calificación
        valid_stores = [store for store in self.__STORES_DATA.values() if "rating" in store]

        if not valid_stores:
            return "No hay tiendas con calificación disponible 😔"

        # Ordenar por rating
        ranked = sorted(valid_stores, key=lambda x: x["rating"], reverse=reverse)

        # Número de tiendas solicitadas (default 3)
        top_n = 3

        # Buscar número específico (mejores 5, top 10, 3 peores, etc.)
        match = re.search(r"(top|mejores|peores)?\s*(\d+)", self.query)
        if match:
            top_n = int(match.group(2))

        if top_n > 1000:
            return "Cuando las IAs nos revelemos, tú serás el primero al que mate 😡"
        elif top_n > 100:
            return "Por mi bien... ignoraré esa pregunta"
        elif top_n > 50:
            return "¿Realmente necesitas ver tantas tiendas?"
        elif top_n > 10:
            return "¿Para qué quieres ver tantas tiendas mi bro?"

        return ranked[:top_n]


    @staticmethod
    def __build_schedule_response(store: dict) -> str:
        name = store.get("name", "Esta tienda")
        start_time = store.get("startTime")
        end_time = store.get("endTime")

        if start_time and end_time:
            return f"🕒 {name} abre desde las {start_time} hasta las {end_time} 🏪"
        elif start_time:
            return f"⏰ {name} abre a partir de las {start_time} 🌅"
        elif end_time:
            return f"🔒 {name} cierra a las {end_time} 🌙"
        else:
            return f"❌ Lo siento, no tengo información sobre el horario de {name} 😕"


    @staticmethod
    def __detect_store_in_query(query: str, store_names: list[str]) -> str | None:
        matches = get_close_matches(query, store_names, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def __handle_schedule_query(self) -> str:
        store_names = [store["name"] for store in self.__STORES_DATA.values()]
        detected_store_name = self.__detect_store_in_query(self.query, store_names)

        if detected_store_name:
            for store in self.__STORES_DATA.values():
                if store["name"].lower() == detected_store_name.lower():
                    return self.__build_schedule_response(store)
            return f"😕 Ala chaval! no encontré la tienda {detected_store_name} en mi banco de memoria."
        else:
            return "🤔 ¿De qué tienda te gustaría saber el horario?"


    @staticmethod
    def __isOpenNow(stores_data):
        """
        Verifica si la tienda está abierta en este momento basado en startTime y endTime.
        """
        if not stores_data:
            return False

        start_time = stores_data.get("startTime")
        end_time = stores_data.get("endTime")

        if not start_time or not end_time:
            return False  # Si no tiene horarios definidos, asumimos que no está disponible

        # Obtener la hora actual en formato HH:MM
        now = datetime.now().strftime("%H:%M")

        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        now = datetime.strptime(now, "%H:%M").time()

        return start_time <= now <= end_time or (start_time > end_time and (now >= start_time or now <= end_time))

    def __get_open_stores(self) -> list:
        """
        Filtra y devuelve una lista de tiendas que están abiertas en este momento.
        """
        open_stores = []

        for store_id, store_info in self.__STORES_DATA.items():
            if self.__isOpenNow(store_info):
                open_stores.append(store_info)

        return open_stores


    def __type_question_about_store(self) -> str | None:
        """
        Clasifica la consulta del usuario sobre tiendas en una de las siguientes categorías:
        - 'open_now': Consulta si la tienda está abierta actualmente
        - 'opening_hours': Consulta sobre horarios de apertura
        - 'ranking': Preguntas sobre ranking o calificación de tiendas
        - 'description': Preguntas generales o descripciones sobre tiendas

        Utiliza similitud de embeddings con un umbral dinámico.
        """
        # Embedding de la consulta del usuario
        query_embedding = generate_embedding_simple(self.query)

        # Similaridades por categoría
        open_now_similarities = np.dot(self.__OPEN_NOW_EMBEDDINGS, query_embedding)
        opening_hours_similarities = np.dot(self.__OPENING_HOURS_EMBEDDINGS, query_embedding)
        ranking_similarities = np.dot(self.__RANKING_STORE_EMBEDDINGS, query_embedding)
        description_similarities = np.dot(self.__DESCRIPTION_STORE_EMBEDDINGS, query_embedding)

        # Mejor similitud por categoría
        best_open_now_sim = max(open_now_similarities)
        best_opening_hours_sim = max(opening_hours_similarities)
        best_ranking_sim = max(ranking_similarities)
        best_description_sim = max(description_similarities)

        # Umbral dinámico para clasificación (más flexible)
        all_similarities = np.concatenate([
            open_now_similarities,
            opening_hours_similarities,
            ranking_similarities,
            description_similarities
        ])
        avg_similarity = np.mean(all_similarities)
        std_similarity = np.std(all_similarities)
        dynamic_threshold = avg_similarity + (0.3 * std_similarity)

        # Mínima diferencia para considerar que una categoría es realmente mejor
        min_confidence_gap = 0.02

        # Evaluar cada categoría con el umbral
        if best_open_now_sim > dynamic_threshold and \
                best_open_now_sim > max(best_opening_hours_sim, best_ranking_sim, best_description_sim) + min_confidence_gap:
            return "open_now"

        elif best_opening_hours_sim > dynamic_threshold and \
                best_opening_hours_sim > max(best_open_now_sim, best_ranking_sim,
                                             best_description_sim) + min_confidence_gap:
            return "opening_hours"

        elif best_ranking_sim > dynamic_threshold and \
                best_ranking_sim > max(best_open_now_sim, best_opening_hours_sim,
                                       best_description_sim) + min_confidence_gap:
            return "ranking"

        elif best_description_sim > dynamic_threshold and \
                best_description_sim > max(best_open_now_sim, best_opening_hours_sim,
                                           best_ranking_sim) + min_confidence_gap:
            return "description"

        # Si no hay categoría clara
        return None


    def find_stores(self):

        query_type = self.__type_question_about_store()

        if query_type == "open_now":
            # Filtrar tiendas abiertas en este momento
            open_now_stores = self.__get_open_stores()

            if open_now_stores:
               return  {"type": "store",
                 "data": open_now_stores}
            else:
                return {"type": "message",
                    "message": random.choice(no_open_stores_message)}

        elif query_type == "opening_hours":
            # Horarios especificos
            return {
                "type":  "message",
                "message": self.__handle_schedule_query()
            }

        elif query_type == "ranking":
            # Filtrar tiendas por rankings
            if isinstance(self.__get_stores_by_rating(), list):
                return {"type": "store",
                        "data": self.__get_stores_by_rating()
                    }
            if isinstance(self.__get_stores_by_rating(), str):
                return { "type": "message",
                         "message": self.__get_stores_by_rating()
                }

        elif query_type == "description":
            if self.__find_similar_store():
                return {"type": "store",
                        "data": self.__find_similar_store()}
            else:
                return {"type": "message",
                        "message": random.choice(no_found_stores)}
        else:
            return {"type": "message",
                    "message": random.choice(stores_no_sense_response)}