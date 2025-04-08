from fastapi import APIRouter
import core.botSingleton as bot

router = APIRouter()

@router.get("/query")
async def get_recommendations(query: str):
   if bot.chat_bot_instance is None:
      raise Exception("El bot no ha sido inicializado")

   return bot.chat_bot_instance.process_query(query)