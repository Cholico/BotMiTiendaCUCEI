import torch
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.constants import ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_NAME
from core.constants import ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_VALUE
from core.constants import SENTIMENT_ANALYZER_MODEL_NAME
from core.constants import SENTIMENT_ANALYZER_LABEL_VERY_NEGATIVE
from core.constants import SENTIMENT_ANALYZER_LABEL_NEGATIVE
from core.constants import SENTIMENT_ANALYZER_LABEL_NEUTRAL
from core.constants import SENTIMENT_ANALYZER_LABEL_POSITIVE
from core.constants import SENTIMENT_ANALYZER_LABEL_VERY_POSITIVE
from domain.model.baseReviewDomain import BaseReviewDomain

os.environ[ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_NAME] = ENVIRON_HF_HUB_DISABLE_SYMLINKS_WARNING_VALUE

# Cargar el tokenizador y el modelo preentrenado de Hugging Face
model_name = SENTIMENT_ANALYZER_MODEL_NAME
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def feeling_review(element: BaseReviewDomain) -> BaseReviewDomain:
    if element.comment is None or element.comment == "":
        # Manejar casos donde el comentario no existe o está vacío
        element.sentiment = ""
        element.comment = ""
        return element
    
    try:
        # Tokenización del comentario
        inputs = tokenizer(element.comment, return_tensors="pt", truncation=True, padding=True)

        # Pasar los tokens por el modelo para obtener las predicciones
        outputs = model(**inputs)

        # Obtener las probabilidades de las emociones
        probs = torch.softmax(outputs.logits, dim=1).detach().numpy()[0]

        # Etiquetas de las emociones (en este modelo, hay 5 niveles de sentimiento)
        labels = [
            SENTIMENT_ANALYZER_LABEL_VERY_NEGATIVE, 
            SENTIMENT_ANALYZER_LABEL_NEGATIVE, 
            SENTIMENT_ANALYZER_LABEL_NEUTRAL, 
            SENTIMENT_ANALYZER_LABEL_POSITIVE, 
            SENTIMENT_ANALYZER_LABEL_VERY_POSITIVE
        ]

        # Determinar la emoción con mayor probabilidad
        element.sentiment = labels[probs.argmax()]
    except Exception as e:
        print(f"Error al procesar el comentario: {e}")
        element.sentiment = ""
    finally:
        return element
