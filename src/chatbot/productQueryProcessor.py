import random
import re
from chatbot.responses import get_confused_message
from chatbot.categories import CATEGORY_SYNONYMS
from data.service.featuresIndexingService import generate_embedding_simple
import data.service.featuresIndexingService as indexig

class ProductQueryProcessor:
    def __init__(self, query: str, product_ids: list, products_data: dict):
        self.query = query
        self.__PRODUCT_IDS = product_ids
        self.__PRODUCTS_DATA = products_data
        self.__CATEGORY_INDEX = indexig.CATEGORY_INDEX
        self.__CATEGORY_LIST = indexig.CATEGORY_LIST
        self.__DEESCRIPTION_INDEX = indexig.DEESCRIPTION_INDEX
        self.__DESCRIPTION_IDS = indexig.DESCRIPTION_IDS

    @staticmethod
    def __sort_by_filter(min_price: float | None, max_price: float | None) -> str | None:
        """
           Determina el orden de los resultados basado en los filtros de precio.
           - Si el usuario quiere productos *desde* un precio → ordenar ascendente.
           - Si el usuario quiere productos *hasta* un precio → ordenar descendente.
           """
        if min_price and not max_price:
            return "asc"  # Usuario busca a partir de cierto precio → ordenar de menor a mayor
        if max_price and not min_price:
            return "desc"  # Usuario busca hasta cierto precio → ordenar de mayor a menor

        # Si hay ambos, o ninguno, no forzar orden
        return None


    def __search_by_description_fallback(self):
        query_embedding = generate_embedding_simple(self.query).reshape(1, -1)

        # Si el índice no ha sido creado, devolver una lista vacía o productos por defecto
        if self.__DEESCRIPTION_INDEX is None or self.__DESCRIPTION_IDS is None:
            return []

        # Realizar la búsqueda utilizando el índice FAISS
        distances, idxs = self.__DEESCRIPTION_INDEX.search(query_embedding, 5)

        # Devolver los ids de los productos más cercanos
        return [self.__DESCRIPTION_IDS[i] for i in idxs[0]]

    def __filter_products(self, min_price: float | None, max_price: float | None,
                        categories: list[str] | None) -> list[str]:
        filtered_ids = []


        for product_id, product in self.__PRODUCTS_DATA.items():
            price = product.get("price")
            passes_price = True  # Por defecto pasa, a menos que se aplique un filtro

            # Filtrado por precio
            if price is not None:
                if min_price is not None and max_price is not None:
                    passes_price = min_price <= price <= max_price
                elif min_price is not None:
                    passes_price = price <= min_price
                elif max_price is not None:
                    passes_price = price >= max_price

            # Filtrado por categoría
            product_category_matches = True  # Por defecto pasa, a menos que se aplique un filtro

            if categories:
                categories = [cat.strip().lower() for cat in categories]
                product_categories = product.get("category", [])
                product_category_matches = False
                for prod_cat in product_categories:
                    if any(cat in prod_cat.lower() for cat in categories):
                        product_category_matches = True
                        break

            # Incluir solo si pasa ambos filtros
            if passes_price and product_category_matches:
                filtered_ids.append(product_id)

        return filtered_ids

    @staticmethod
    def __check_quantity_limits(quantity: int) -> dict | None:
        if quantity > 1000:
            return {"type": "message",
                    "message": f"¿Top {quantity}? Jajajajaja JAJAJA ay no, qué bárbaro, qué ocurrente... ya pide algo con sentido 😆"}
        elif quantity > 100:
            return {"type": "message", "message": f"¿Top {quantity}? 😳 Eso ya no es top, es enciclopedia."}
        elif quantity > 50:
            return {"type": "message", "message": "El chiste de un top es que sea breve, amigo 🤓"}
        elif quantity > 10:
            return {"type": "message",
                    "message": f"En mi humilde opinión, un top {quantity} no tiene mucho sentido... ¿qué tal algo más breve? 😅"}
        return None

    @staticmethod
    def filter_by_rating(products_data: dict, ids:list, quality: str, quantity: int) -> list[str]:
        # Validar que calidad y cantidad sean válidos
        if not quality or not quantity or not ids:
            return ids

        # Ordenar los productos por rating
        sorted_ids = sorted(
            ids,
            key=lambda pid: products_data[pid].get("rating", 0),
            reverse=(quality == "mejor")
        )

        # Devolver los primeros `quantity`
        return sorted_ids[:quantity]

    def __detect_rating(self) -> tuple[str | None, int | None]:

        # Detectar si quiere los mejores productos
        if re.search(r'\b(mejor(es)?|top|buenos|excelentes|recomendados)\b', self.query):
            match = re.search(r'\b(\d+)\b', self.query)
            cantidad = int(match.group(1)) if match else 3
            return "mejor", cantidad

        # Detectar si quiere los peores productos
        if re.search(r'\b(peor(es)?|malos|malas|horribles|terribles)\b', self.query):
            match = re.search(r'\b(\d+)\b', self.query)
            cantidad = int(match.group(1)) if match else 3
            return "peor", cantidad

        # Si no encuentra palabras clave pero hay un número suelto, lo asume como cantidad de mejores
        match = re.search(r'\b(\d+)\b', self.query)
        if match:
            return "mejor", int(match.group(1))

        return None, None


    def __detect_categories(self) -> list[str]:
        detected = set()

        # Búsqueda directa por sinónimos o nombres
        for category, synonyms in CATEGORY_SYNONYMS.items():
            if category in self.query:
                detected.add(category)
            elif any(syn in self.query for syn in synonyms):
                detected.add(category)

        # Si ya se detectaron categorías directamente, no usar FAISS (más preciso)
        if detected:
            return list(detected)

        # Si no se detectó nada directo, usar embeddings
        query_embedding = generate_embedding_simple(self.query).reshape(1, -1)
        distances, indices = self.__CATEGORY_INDEX.search(query_embedding, 5)

        for i, idx in enumerate(indices[0]):
            category = self.__CATEGORY_LIST[idx]
            distance = distances[0][i]

            if distance < 0.15:
                detected.add(category)

        return list(detected)

    # Rangos de precio
    @staticmethod
    def __extract_price_range(query: str) -> tuple:

        # 1. Detectar expresiones como "entre 100 y 150" (con o sin pesos)
        match = re.search(r'entre\s+\$?(\d+(?:\.\d{1,2})?)\s+(?:y|a)\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 2. Detectar expresiones como "de 100 a 200"
        match = re.search(r'de\s+\$?(\d+(?:\.\d{1,2})?)\s+(?:a|y)\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 3. Detectar expresiones como "más de 100 y menos de 200"
        match = re.search(r'más\s+de\s+\$?(\d+(?:\.\d{1,2})?).*?menos\s+de\s+\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?',
                          query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # 4. Detectar expresiones como "$100 a $200" o "100 - 200"
        match = re.search(r'\$?(\d+(?:\.\d{1,2})?)\s*(?:-|a|–|—)\s*\$?(\d+(?:\.\d{1,2})?)\s*(?:pesos)?', query)
        if match:
            return float(match.group(1)), float(match.group(2))

        # No se detectó un rango
        return None, None


    def __detect_price(self) -> tuple:
        # 1. Buscar rango como "entre 50 y 100"
        min_price, max_price = self.__extract_price_range(self.query)
        if min_price is not None and max_price is not None:
            return min_price, max_price

        # 2. "más de X" → max_price = X
        match = re.search(r'(más de|mas de|desde|por más de|por mas de)\s+\$?(\d+(?:\.\d{1,2})?)', self.query)
        if match:
            return None, float(match.group(2))

        # 3. "menos de X" → min_price = X
        match = re.search(r'(menos de|hasta|por menos de)\s+\$?(\d+(?:\.\d{1,2})?)', self.query)
        if match:
            return float(match.group(2)), None

        # 4. Número suelto → interpretado como max_price
        match = re.search(r'\b(\d+(?:\.\d{1,2})?)\b', self.query)
        if match:
            return None, float(match.group(1))

        return None, None


    # Funcion para extraer los filtros de la query
    def __extract_filters_from_query(self) -> tuple:
        min_price, max_price = self.__detect_price()
        category = self.__detect_categories()
        quality, quantity = self.__detect_rating()

        return min_price, max_price, category, quality, quantity

    def find_products(self, top_k: int = 10) -> dict:

        # Extraer filtros de la pregunta (que le interesa saber al cliente)
        min_price, max_price, category, quality, quantity = self.__extract_filters_from_query()

        # Checa que si en caso que el usuario pida una catidad de productos a ver no sea demasiada exagerada
        reting_check = self.__check_quantity_limits(quantity)
        if reting_check:
            return reting_check

        # Verificar si todos los filtros están vacíos de ser el caso la pregunta debe de tener algo mal
        if not any([min_price, max_price, category, quality, quantity]):
            return {"type": "message",
                    "message": random.choice(get_confused_message)}

        # En base a los filtros obtner los ids
        filtered_ids = self.__filter_products(min_price, max_price, category)

        # Filtado por calidad
        if quality and quantity and filtered_ids:
            filtered_ids = self.filter_by_rating(self.__PRODUCTS_DATA, filtered_ids, quality, quantity)
        elif quantity and quality:
            filtered_ids = self.filter_by_rating(self.__PRODUCTS_DATA, self.__PRODUCT_IDS, quality, quantity)

        # Realizar la búsqueda por descripción utilizando FAISS si es necesario
        description_results = self.__search_by_description_fallback()

        # Combina los resultados de los filtros con los resultados por descripción
        combined_ids = set(filtered_ids) | set(description_results)

        # Filtrar productos según los ids combinados
        result = [self.__PRODUCTS_DATA[prod_id] for prod_id in combined_ids]

        order = self.__sort_by_filter(min_price, max_price)

        if order == "asc":
            result.sort(key=lambda p: p["price"])
        elif order == "desc":
            result.sort(key=lambda p: p["price"], reverse=True)

        if not result:
            return {"type": "message",
                "message": random.choice(get_confused_message)}

        return {"type": "product", "data": result[:top_k]}