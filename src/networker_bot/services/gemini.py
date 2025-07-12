import google.generativeai as genai
import os
import json
import logging
from networker_bot.config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class GeminiService:
    """Servicio para extraer información estructurada usando Gemini 1.5 Flash"""
    
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    async def extract_info(self, transcript: str) -> dict:
        """
        Extrae información estructurada del transcript de audio.
        
        Args:
            transcript (str): Texto transcrito del audio
            
        Returns:
            dict: Diccionario con información del usuario
            
        Raises:
            Exception: Si hay error en la API o parsing JSON
        """
        try:
            prompt = f"""
            Analiza esta presentación personal y extrae la información más relevante para cada campo.
            La persona puede presentarse de manera formal, informal, completa o parcial.
            
            AUDIO TRANSCRITO:
            "{transcript}"
            
            INSTRUCCIONES:
            - Analiza el contenido y mapea la información a los campos correspondientes
            - Si no hay información clara para un campo, usa "No especificado"
            - Información relevante que no encaje en campos específicos va en "info_adicional"
            - Sé flexible con diferentes formas de expresar la misma información
            
            CAMPOS A COMPLETAR:
            - nombre: Nombre completo o como se presenta la persona
            - edad: Edad numérica, rango de edad, o "No especificado"
            - ocupacion: Trabajo, profesión, carrera, estudios, o rol principal
            - proyecto: Proyecto actual, trabajo en curso, startup, idea, o actividad principal
            - stack: Tecnologías, herramientas, lenguajes, frameworks, áreas de expertise, habilidades técnicas
            - hobby: Pasatiempos, intereses personales, deportes, aficiones
            - info_adicional: Cualquier información relevante que no encaje en los campos anteriores (ubicación, experiencia, metas, context del hackaton, etc.)
            
            EJEMPLOS DE MAPEO:
            - "Soy de México" → info_adicional: "De México"
            - "Llevo 5 años programando" → info_adicional: "5 años de experiencia programando"
            - "Quiero aprender IA" → info_adicional: "Interesado en aprender IA"
            - "Vine al hackaton para conocer gente" → info_adicional: "Participante del hackaton, busca networking"
            
            RETORNA SOLO UN JSON VÁLIDO CON ESTOS CAMPOS:
            {{
                "nombre": "...",
                "edad": "...",
                "ocupacion": "...",
                "proyecto": "...",
                "stack": "...",
                "hobby": "...",
                "info_adicional": "..."
            }}
            
            IMPORTANTE: Solo retorna el JSON, sin explicaciones adicionales.
            """
            
            response = self.model.generate_content(prompt)
            
            # Limpiar respuesta y parsear JSON
            clean_response = response.text.strip()
            if clean_response.startswith('```json'):
                clean_response = clean_response[7:-3]
            elif clean_response.startswith('```'):
                clean_response = clean_response[3:-3]
            
            user_data = json.loads(clean_response)
            logger.info(f"Información extraída: {user_data.get('nombre', 'Sin nombre')}")
            
            return user_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON de Gemini: {e}")
            raise Exception(f"Error al parsear respuesta de Gemini: {str(e)}")
        except Exception as e:
            logger.error(f"Error en Gemini API: {e}")
            raise Exception(f"Error al extraer información: {str(e)}")
