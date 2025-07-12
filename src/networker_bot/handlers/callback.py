import logging
from telegram import Update
from telegram.ext import ContextTypes

from networker_bot.config import ORGANIZER

logger = logging.getLogger(__name__)

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Maneja los callbacks de los botones del bot.
    
    Args:
        update: Objeto Update de Telegram
        context: Contexto de la conversación
    """
    try:
        query = update.callback_query
        await query.answer()  # Confirmar que se recibió el callback
        
        if query.data == 'start_recording':
            instruction_message = """
🎤 **¡Perfecto! Ahora graba tu presentación**

**Incluye en tu voice note:**
• Tu nombre completo
• Tu edad
• Tu ocupación/profesión
• Proyecto actual en el que trabajas
• Stack tecnológico o área de expertise
• Hobby o dato curioso sobre ti

**Ejemplo:**
*"Hola, soy María González, tengo 28 años, soy desarrolladora fullstack, actualmente trabajo en un proyecto de e-commerce usando React y Node.js, y en mi tiempo libre me gusta practicar surf"*

🎙️ **Envía tu voice note ahora** 👇

⏱️ **Recomendación:** Habla entre 30-60 segundos para mejores resultados.
            """
            
            await query.edit_message_text(
                instruction_message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Usuario {update.effective_user.id} presionó 'Grabar Presentación'")
        
        else:
            # Callback desconocido
            await query.edit_message_text(
                "❌ Acción no reconocida. Envía /start para comenzar de nuevo."
            )
            logger.warning(f"Callback desconocido: {query.data}")
            
    except Exception as e:
        logger.error(f"Error en callback_handler: {e}")
        try:
            await update.callback_query.edit_message_text(
                "❌ Error al procesar la acción. Envía /start para intentar de nuevo."
            )
        except:
            pass  # Si no se puede editar el mensaje, no hacer nada
