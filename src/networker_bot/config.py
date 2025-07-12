import os
from dotenv import load_dotenv

load_dotenv()

# Configuración del bot
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GOOGLE_SHEETS_ID = os.getenv('GOOGLE_SHEETS_ID')

# Configuración del evento
EVENT_NAME = os.getenv('EVENT_NAME', 'Hackaton Release Before Ready')
ORGANIZER = os.getenv('ORGANIZER', 'opino.tech')

# Validar que todas las variables estén presentes
required_vars = [
    'TELEGRAM_BOT_TOKEN',
    'DEEPGRAM_API_KEY', 
    'GEMINI_API_KEY',
    'GOOGLE_SHEETS_ID'
]

for var in required_vars:
    if not os.getenv(var):
        raise ValueError(f"Variable de entorno {var} no encontrada")
