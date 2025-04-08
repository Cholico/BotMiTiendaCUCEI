from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
import os
import asyncio
import fireo

from core.firebaseHelper import db
from core.constants import REDIS_CACHE_PREFIX
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

# Inicializa modelo ANTES de importar cualquier módulo que lo use
from core.modelSingleton import init_embedding_model
init_embedding_model()

# Ahora puedes importar servicios que dependen del modelo
from data.service.indexing import refresh_faiss_index_stores, refresh_faiss_index_products, periodic_faiss_refresh
from data.service.questionsEmbeddingsService import generate_question_embeddings
from data.service.featuresIndexingService import ensure_category_index_initialized, build_description_faiss_index, refresh_description_index
from core.botSingleton import init_bot
from routes.storeReviewRoutes import router as store_review_router
from routes.productReviewRoutes import router as product_review_router
from routes.insightRoutes import router as insight_router
from controllers.recommenderController import router as recommender_router
from routes.botRoute import api_router as bot_query

load_dotenv()

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    REDIS_SERVER_URL = os.getenv("REDIS_SERVER_URL", "redis://localhost:6379")
    try:
        redis = aioredis.from_url(REDIS_SERVER_URL, encoding="utf-8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix=REDIS_CACHE_PREFIX)
        print("Redis cache inicializado correctamente")
    except Exception as e:
        print(f"No se pudo conectar a Redis: {e}")

    # Construir el índice FAISS al iniciar
    try:
        refresh_faiss_index_products()
        refresh_faiss_index_stores()
        print("Índice FAISS de productos generado correctamente al iniciar.")
    except Exception as e:
        print(f"Error al generar índice FAISS de productos: {e}")

    # Genera los embeddings para el bot
    generate_question_embeddings()
    # Generar embeddings de categoria
    ensure_category_index_initialized()
    # Generar embeddings de descripciones
    build_description_faiss_index()
    # Inicializa el bot
    init_bot()


    # Tarea de refresco periódico
    asyncio.create_task(periodic_faiss_refresh(interval_seconds=1800))
    asyncio.create_task(refresh_description_index(interval_seconds=3600))

    yield  # Continúa ejecutando FastAPI sin bloquear por Redis

fireo.connection(client=db)
app = FastAPI(lifespan=lifespan)

app.include_router(store_review_router, tags=["store_reviews"])
app.include_router(product_review_router, tags=["product_reviews"])
app.include_router(insight_router, tags=["insights"])
app.include_router(recommender_router, tags=["recommendations"])
app.include_router(bot_query, tags=['ask'])
