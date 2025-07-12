import logging
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from networker_bot.services.deepgram import DeepgramService
from networker_bot.services.gemini import GeminiService
from networker_bot.services.sheets import SheetsService

logger = logging.getLogger(__name__)

deepgram_service = DeepgramService()
gemini_service = GeminiService()
sheets_service = SheetsService()

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Procesa notas de voz y extrae información para networking"""
    
    if not update.message or not update.message.voice:
        return
    
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Enviar mensaje de procesamiento
    processing_msg = await update.message.reply_text(
        "🎧 Procesando tu presentación...\n"
        "⏳ Esto puede tomar unos segundos."
    )
    
    try:
        # 1. Descargar el archivo de audio
        voice_file = await update.message.voice.get_file()
        
        # Crear directorio temporal si no existe
        os.makedirs("temp", exist_ok=True)
        
        # Descargar archivo
        file_path = f"temp/voice_{user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg"
        await voice_file.download_to_drive(file_path)
        
        logger.info(f"Audio descargado: {file_path}")
        
        # 2. Transcribir audio con Deepgram
        await processing_msg.edit_text(
            "🎧 Audio descargado\n"
            "📝 Transcribiendo..."
        )
        
        transcript = await deepgram_service.transcribe_audio(file_path)
        
        if not transcript:
            await processing_msg.edit_text(
                "❌ No se pudo transcribir el audio.\n"
                "Por favor, intenta de nuevo con una nota de voz más clara."
            )
            return
        
        logger.info(f"Transcripción completada: {transcript[:100]}...")
        
        # 3. Extraer información estructurada con Gemini
        await processing_msg.edit_text(
            "🎧 Audio descargado ✅\n"
            "📝 Transcripción completada ✅\n"
            "🤖 Extrayendo información..."
        )
        
        structured_info = await gemini_service.extract_info(transcript)  # type: ignore[attr-defined]
        
        if not structured_info:
            await processing_msg.edit_text(
                "❌ No se pudo extraer información estructurada.\n"
                "Por favor, intenta de nuevo con una presentación más detallada."
            )
            return
        
        logger.info(f"Información extraída: {structured_info}")
        
        # 4. Preparar datos para Google Sheets
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row_data = [
            structured_info.get("nombre", ""),
            structured_info.get("edad", ""),
            structured_info.get("ocupacion", ""),
            structured_info.get("proyecto", ""),
            structured_info.get("stack", ""),
            structured_info.get("hobby", ""),
            structured_info.get("info_adicional", ""),
            structured_info.get('lugar_conocimos', ''),  # ← Cambiado
            current_time,                      # Fecha/Hora
            user.username or "",               # Username
            str(user.id)                       # User ID
        ]
        
        # 5. Guardar en Google Sheets
        await processing_msg.edit_text(
            "🎧 Audio descargado ✅\n"
            "📝 Transcripción completada ✅\n"
            "🤖 Información extraída ✅\n"
            "📊 Guardando en base de datos..."
        )
        
        success = await sheets_service.add_row(row_data)  # type: ignore[attr-defined]
        
        if success:
            # Mostrar resumen al usuario
            summary_text = "✅ **¡Presentación procesada exitosamente!**\n\n"
            summary_text += "📋 **Información extraída:**\n"
            
            if structured_info.get("nombre"):
                summary_text += f"👤 **Nombre:** {structured_info['nombre']}\n"
            if structured_info.get("edad"):
                summary_text += f"🎂 **Edad:** {structured_info['edad']}\n"
            if structured_info.get("ocupacion"):
                summary_text += f"💼 **Ocupación:** {structured_info['ocupacion']}\n"
            if structured_info.get("proyecto"):
                summary_text += f"🚀 **Proyecto:** {structured_info['proyecto']}\n"
            if structured_info.get("stack"):
                summary_text += f"⚡ **Stack/Expertise:** {structured_info['stack']}\n"
            if structured_info.get("hobby"):
                summary_text += f"🎯 **Hobby/Dato Curioso:** {structured_info['hobby']}\n"
            
            summary_text += "\n🎉 **¡Tu información ha sido guardada para networking!**"
            
            await processing_msg.edit_text(summary_text, parse_mode="Markdown")
            
            # Ofrecer enviar otra presentación
            await update.message.reply_text(
                "¿Quieres enviar otra presentación? 🎤\n"
                "Simplemente envía otra nota de voz o usa /start para ver el menú."
            )
            
        else:
            await processing_msg.edit_text(
                "❌ Error al guardar la información.\n"
                "Por favor, intenta de nuevo."
            )
        
    except Exception as e:
        logger.error(f"Error procesando nota de voz: {str(e)}")
        await processing_msg.edit_text(
            "❌ Ocurrió un error al procesar tu presentación.\n"
            "Por favor, intenta de nuevo."
        )
    
    finally:
        # Limpiar archivo temporal
        try:
            if 'file_path' in locals() and os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Archivo temporal eliminado: {file_path}")
        except Exception as e:
            logger.error(f"Error eliminando archivo temporal: {str(e)}")
