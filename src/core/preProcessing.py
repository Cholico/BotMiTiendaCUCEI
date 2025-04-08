import re
from domain.model.baseReviewDomain import BaseReviewDomain

def cleaning_review(element: BaseReviewDomain) -> BaseReviewDomain:
    if element.comment is None or element.comment == "":
        element.comment = "" # Manejar casos donde el comentario no existe o está vacío
        return element

    # Normalizar el texto (convertir a minúsculas)
    element.comment = element.comment.lower()

    # Eliminar caracteres no alfanuméricos, excepto los espacios
    element.comment = re.sub(r'[^a-zA-Z0-9\s]', '', element.comment)

    # Eliminar espacios extra
    element.comment = re.sub(r'\s+', ' ', element.comment).strip()

    return element