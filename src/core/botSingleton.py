from chatbot.chatBot import ChatBot

chat_bot_instance = None  # Variable global

def init_bot():
    global chat_bot_instance
    chat_bot_instance = ChatBot()