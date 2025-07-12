import os
import logging
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions

load_dotenv()

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
logger = logging.getLogger(__name__)

class DeepgramService:
    def __init__(self):
        self.client = DeepgramClient(DEEPGRAM_API_KEY)
        logger.info("✅ DeepgramService inicializado correctamente")
    
    async def transcribe_audio(self, file_path: str) -> str:
        """
        Transcribe audio file to text using Deepgram API.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        try:
            logger.info(f"🎵 Iniciando transcripción de: {file_path}")
            
            # Verificar que el archivo existe
            if not os.path.exists(file_path):
                logger.error(f"❌ Archivo no encontrado: {file_path}")
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
            
            # Verificar tamaño del archivo
            file_size = os.path.getsize(file_path)
            logger.info(f"📊 Tamaño del archivo: {file_size} bytes")
            
            # Configurar opciones de transcripción
            logger.info("⚙️ Configurando opciones de transcripción...")
            options = PrerecordedOptions(
                model="nova-2",
                language="es",
                smart_format=True,
                punctuate=True,
                diarize=False
            )
            logger.info("✅ Opciones configuradas")
            
            # Leer archivo de audio
            logger.info(f"📖 Leyendo archivo: {file_path}")
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            logger.info(f"✅ Archivo leído: {len(audio_data)} bytes")
            
            # Probar diferentes sintaxis de la API
            logger.info("🔄 Intentando transcribir con Deepgram...")
            
            # Opción 1: Sintaxis más simple
            try:
                logger.info("🔄 Probando sintaxis v1...")
                response = self.client.listen.prerecorded.v("1").transcribe_file(
                    audio_data,
                    options
                )
                logger.info("✅ Sintaxis v1 exitosa")
            except Exception as e1:
                logger.error(f"❌ Sintaxis v1 falló: {e1}")
                
                # Opción 2: Sintaxis alternativa  
                try:
                    logger.info("🔄 Probando sintaxis v2...")
                    response = self.client.listen.rest.v("1").transcribe_file(
                        audio_data,
                        options
                    )
                    logger.info("✅ Sintaxis v2 exitosa")
                except Exception as e2:
                    logger.error(f"❌ Sintaxis v2 falló: {e2}")
                    
                    # Opción 3: Usando payload dict
                    try:
                        logger.info("🔄 Probando sintaxis v3 con payload...")
                        payload = {"buffer": audio_data}
                        response = self.client.listen.prerecorded.v("1").transcribe_file(
                            payload,
                            options
                        )
                        logger.info("✅ Sintaxis v3 exitosa")
                    except Exception as e3:
                        logger.error(f"❌ Sintaxis v3 falló: {e3}")
                        raise Exception(f"Todos los métodos fallaron: v1={e1}, v2={e2}, v3={e3}")
            
            # Extraer texto transcrito
            logger.info("📝 Procesando respuesta...")
            logger.info(f"🔍 Tipo de respuesta: {type(response)}")
            
            if hasattr(response, 'results') and response.results:
                logger.info("✅ Respuesta contiene resultados")
                if hasattr(response.results, 'channels') and response.results.channels:
                    logger.info(f"✅ Encontrados {len(response.results.channels)} canales")
                    if response.results.channels[0].alternatives:
                        transcript = response.results.channels[0].alternatives[0].transcript
                        logger.info(f"🎉 Transcripción exitosa: {len(transcript)} caracteres")
                        logger.info(f"📝 Transcripción: {transcript[:100]}...")
                        return transcript
                    else:
                        logger.error("❌ No hay alternativas en el canal")
                else:
                    logger.error("❌ No hay canales en los resultados")
            else:
                logger.error("❌ No hay resultados en la respuesta")
                logger.error(f"🔍 Respuesta completa: {response}")
            
            logger.error("❌ No se pudo obtener transcripción del audio")
            return ""
                
        except Exception as e:
            logger.error(f"💥 Error crítico al transcribir audio: {e}")
            logger.error(f"🔍 Tipo de error: {type(e)}")
            import traceback
            logger.error(f"🔍 Traceback: {traceback.format_exc()}")
            raise Exception(f"Error al transcribir audio: {e}")
