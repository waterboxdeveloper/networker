import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from telegram import Update

from networker_bot.config import TELEGRAM_BOT_TOKEN
from networker_bot.handlers.start import start_handler
from networker_bot.handlers.callback import callback_handler
from networker_bot.handlers.voice import voice_handler
import os

# Crear directorio temp si no existe
os.makedirs("temp", exist_ok=True)

# Configurar logging más detallado
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """
    Función principal del bot
    """
    try:
        # Crear aplicación
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Registrar handlers
        application.add_handler(CommandHandler("start", start_handler))
        application.add_handler(CallbackQueryHandler(callback_handler))
        application.add_handler(MessageHandler(filters.VOICE, voice_handler))
        
        # Iniciar bot
        logger.info("🤖 Networker Bot iniciado en producción")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"💥 Error crítico al iniciar bot: {e}")
        raise

if __name__ == '__main__':
    main() 