## 🚀 Arranque del backend

### Requisitos previos
- Python 3.11
- uv instalado (pip install uv)
- API Key de Groq: https://console.groq.com
- (Opcional) API Key de HuggingFace: https://huggingface.co/settings/tokens

---

## Pasos

### 1. Entrar en la carpeta backend

cd backend

---

### 2. Crear entorno virtual e instalar dependencias

uv venv --python 3.11
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
uv sync

---

### 3. Configurar variables de entorno

Crea el archivo .env a partir del ejemplo:

cp .env.example .env

Edita el archivo .env y añade al menos:

GROQ_API_KEY=tu_groq_key

Si quieres habilitar generación de imágenes con IA:

HF_API_KEY=tu_huggingface_token

---

### 4. Ejecutar el servidor en modo desarrollo

export PYTHONPATH=src
uvicorn src.app.main:app --reload --port 8000

En Windows (PowerShell):

$env:PYTHONPATH="src"
uvicorn src.app.main:app --reload --port 8000

---

### 5. Verificar que el backend funciona

http://localhost:8000/docs

---

## 🧪 Notas adicionales

- Si HF_API_KEY no está configurada, el sistema seguirá funcionando usando fallback automático (Pollinations).
- El sistema de imágenes soporta:
  - Unsplash (imágenes reales)
  - HuggingFace (IA generativa)
  - Pollinations (fallback sin API key)
- Se recomienda usar entorno virtual para evitar conflictos de dependencias.