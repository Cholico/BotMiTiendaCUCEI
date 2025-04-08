from fastapi import APIRouter
from controllers.botController import router as bot_router

api_router = APIRouter()
api_router.include_router(bot_router, prefix="/api", tags=["ask"])