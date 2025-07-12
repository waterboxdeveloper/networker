import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import json

load_dotenv()

GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')
EVENT_NAME = os.getenv('EVENT_NAME', 'Hackaton Release Before Ready')
logger = logging.getLogger(__name__)

class SheetsService:
    """Servicio para guardar información en Google Sheets"""
    
    def __init__(self):
        try:
            # Configurar credenciales
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Intentar desde archivo primero
            if os.path.exists('credentials.json'):
                creds = Credentials.from_service_account_file('credentials.json', scopes=scope)
            else:
                # Si no existe archivo, usar variable de entorno
                creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
                if creds_json:
                    creds_dict = json.loads(creds_json)
                    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
                else:
                    raise Exception("No se encontraron credenciales de Google")
            
            self.client = gspread.authorize(creds)
            self.sheet = self.client.open_by_key(GOOGLE_SHEETS_ID).sheet1
            
        except Exception as e:
            logger.error(f"Error al inicializar SheetsService: {e}")
            raise
    
    async def add_row(self, row_data: list) -> bool:
        """
        Agrega una fila a Google Sheets.
        
        Args:
            row_data (list): Datos a agregar como fila
            
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            self.sheet.append_row(row_data)
            logger.info(f"Fila agregada exitosamente con {len(row_data)} campos")
            return True
            
        except Exception as e:
            logger.error(f"Error al agregar fila: {e}")
            return False
    
    def save_user_data(self, user_data: dict, metadata: dict) -> bool:
        """
        Guarda datos del usuario en Google Sheets.
        
        Args:
            user_data (dict): Datos extraídos por Gemini
            metadata (dict): Información adicional (fecha, username, etc.)
            
        Returns:
            bool: True si se guardó exitosamente
            
        Raises:
            Exception: Si hay error al guardar
        """
        try:
            # Preparar fila según headers de Google Sheets
            row_data = [
                user_data.get('nombre', 'No especificado'),
                user_data.get('edad', 'No especificado'),
                user_data.get('ocupacion', 'No especificado'),
                user_data.get('proyecto', 'No especificado'),
                user_data.get('stack', 'No especificado'),
                user_data.get('hobby', 'No especificado'),
                user_data.get('info_adicional', 'No especificado'),
                metadata.get('lugar_conocimos', EVENT_NAME),
                metadata.get('fecha_hora', datetime.now().strftime("%Y-%m-%d %H:%M")),
                metadata.get('username', 'Sin username'),
                metadata.get('user_id', 'Sin ID')
            ]
            
            # Guardar en Google Sheets
            self.sheet.append_row(row_data)
            
            logger.info(f"Datos guardados exitosamente: {user_data.get('nombre', 'Sin nombre')}")
            return True
            
        except Exception as e:
            logger.error(f"Error al guardar en Sheets: {e}")
            raise Exception(f"Error al guardar en Google Sheets: {str(e)}")
