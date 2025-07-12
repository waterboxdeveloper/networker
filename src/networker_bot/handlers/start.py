import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from networker_bot.config import ORGANIZER

logger = logging.getLogger(__name__)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Maneja el comando /start del bot.
    
    Args:
        update: Objeto Update de Telegram
        context: Contexto de la conversación
    """
    try:
        # Crear botón interactivo
        keyboard = [
            [InlineKeyboardButton("🎤 Grabar Presentación", callback_data='start_recording')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Mensaje de bienvenida
        welcome_message = f"""
🤖 **¡Hola! Soy Networker Bot**

*Powered by {ORGANIZER}*

Automatizo el proceso de networking extrayendo información de tus presentaciones en voice notes.

**¿Cómo funciona?**
1. Presiona el botón "🎤 Grabar Presentación"
2. Envía un voice note presentándote
3. Yo extraigo tu información automáticamente
4. La guardo en una base de datos organizada

**Evento:** Hackaton Release Before Ready

¡Presiona el botón para empezar! 👇
        """
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        logger.info(f"Usuario {update.effective_user.id} ejecutó /start")
        
    except Exception as e:
        logger.error(f"Error en start_handler: {e}")
        await update.message.reply_text(
            "❌ Error al iniciar el bot. Inténtalo de nuevo."
        )
