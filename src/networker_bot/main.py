import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters

from networker_bot.config import TELEGRAM_BOT_TOKEN
from networker_bot.handlers.start import start_handler
from networker_bot.handlers.callback import callback_handler
from networker_bot.handlers.voice import voice_handler

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Inicializa y ejecuta el bot"""
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_handler(MessageHandler(filters.VOICE, voice_handler))
    
    # Ejecutar bot
    logger.info("🤖 Iniciando Networker Bot...")
    application.run_polling(allowed_updates=["message", "callback_query"])

if __name__ == "__main__":
    main() 