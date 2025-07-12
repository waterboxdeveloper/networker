# 🤖 Networker Bot - Automatización de Networking con IA
*Powered by opino.tech*

## 📋 Descripción del Proyecto

**Networker Bot** es un bot de Telegram que automatiza el proceso de networking en hackathons y eventos. Los usuarios envían voice notes presentándose y el bot extrae automáticamente información estructurada guardándola en Google Sheets para facilitar el networking posterior.

### 👨‍🏫 Instructor: Daniel
**Hackathon:** Release Before Ready | **Organización:** opino.tech

## 🎯 ¿Qué hace el bot?

1. **🎤 Recibe voice notes** de presentaciones personales
2. **🔤 Transcribe audio a texto** usando Deepgram API
3. **🧠 Extrae información estructurada** con Google Gemini Flash 1.5
4. **📊 Guarda automáticamente** en Google Sheets
5. **🔄 Procesa en tiempo real** con feedback al usuario

## 🛠️ Stack Tecnológico

- **Language**: Python 3.11+
- **Package Manager**: UV 0.7.2
- **Bot Framework**: `python-telegram-bot` (async)
- **Transcripción**: Deepgram API (modelo nova-2)
- **AI Processing**: Google Gemini Flash 1.5
- **Database**: Google Sheets API
- **Logging**: Python logging con niveles detallados

## 📋 Información Extraída Automáticamente

- **Nombre**
- **Edad**
- **Ocupación**
- **Proyecto actual**
- **Stack/Área de expertise**
- **Hobby/Dato curioso**
- **Información adicional**
- **Lugar donde nos conocimos** (extraído del audio)
- **Fecha/Hora de registro**
- **Username de Telegram**
- **User ID**

## 🏗️ Estructura del Proyecto

```
networker/
├── src/networker_bot/
│   ├── handlers/
│   │   ├── start.py          # Comando /start
│   │   ├── callback.py       # Botones interactivos
│   │   └── voice.py          # Procesamiento de voice notes
│   ├── services/
│   │   ├── deepgram.py       # Transcripción de audio
│   │   ├── gemini.py         # Extracción de información
│   │   └── sheets.py         # Almacenamiento en Google Sheets
│   ├── config.py             # Configuración y variables de entorno
│   └── main.py               # Punto de entrada principal
├── .env                      # Variables de entorno (no incluido en repo)
├── credentials.json          # Credenciales de Google (no incluido en repo)
├── pyproject.toml           # Configuración del proyecto UV
└── run_bot.py               # Script de ejecución
```

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd networker
```

### 2. Instalar dependencias con UV
```bash
uv sync
```

### 3. Configurar variables de entorno
Crear archivo `.env` con:
```env
TELEGRAM_BOT_TOKEN=tu_token_de_telegram
DEEPGRAM_API_KEY=tu_api_key_de_deepgram
GEMINI_API_KEY=tu_api_key_de_gemini
GOOGLE_SHEETS_ID=tu_id_de_google_sheet
```

### 4. Configurar credenciales de Google
- Descargar `credentials.json` desde Google Cloud Console
- Colocar en la raíz del proyecto

### 5. Ejecutar el bot
```bash
uv run python run_bot.py
```

## 🔧 APIs y Servicios Utilizados

### Telegram Bot API
- Creación del bot con BotFather
- Handlers para comandos y mensajes
- Botones interactivos y callbacks

### Deepgram API
- Transcripción de audio con modelo nova-2
- Optimizado para español
- Procesamiento en tiempo real

### Google Gemini Flash 1.5
- Extracción de información estructurada
- Prompts optimizados para presentaciones
- Manejo de diferentes estilos de presentación

### Google Sheets API
- Almacenamiento automático de datos
- Service account authentication
- Headers pre-configurados

## 📊 Flujo de Trabajo

1. Usuario envía `/start` → Bot muestra botón "🎤 Grabar Presentación"
2. Usuario presiona botón → Bot muestra instrucciones
3. Usuario envía voice note → Bot procesa:
   - ✅ Descarga audio
   - ✅ Transcribe con Deepgram
   - ✅ Extrae información con Gemini
   - ✅ Guarda en Google Sheets
4. Usuario recibe confirmación con resumen

## 🎤 Ejemplo de Uso

**Voice Note:** *"Hola, soy María, tengo 25 años, soy desarrolladora Full Stack. Actualmente trabajo en un proyecto de e-commerce usando React y Node.js. Me gusta mucho el rock y tocar guitarra en mi tiempo libre."*

**Resultado en Google Sheets:**
| Nombre | Edad | Ocupación | Proyecto | Stack | Hobby | Lugar | Fecha |
|--------|------|-----------|----------|-------|-------|-------|-------|
| María | 25 | Desarrolladora Full Stack | E-commerce | React, Node.js | Rock, guitarra | Release Before Ready | 2024-07-11 23:30:00 |

## 🚀 Estado del Proyecto

✅ **Completado y Funcional**
- Todos los servicios integrados
- Manejo de errores robusto
- Logging detallado
- Pruebas exitosas

## 🔒 Seguridad

- ⚠️ No incluir archivos `.env` o `credentials.json` en el repositorio
- 🔐 Usar variables de entorno para todas las API keys
- 🔧 Service account para Google Sheets con permisos mínimos

## 📝 Notas de Desarrollo

- **Arquitectura asíncrona** para mejor rendimiento
- **Separación de responsabilidades** por servicios
- **Logging detallado** para debugging
- **Manejo de errores** con feedback al usuario
- **Configuración flexible** mediante variables de entorno

---

**¡Automatiza tu networking con IA!** 🚀

*Proyecto desarrollado en el hackathon "Release Before Ready" - opino.tech*