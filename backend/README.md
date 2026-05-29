## 🚀 Arranque del backend

### Requisitos previos
- Python 3.11
- uv instalado (`pip install uv`)
- API Key de Groq: https://console.groq.com

### Pasos

1. Entra en la carpeta backend:
```bash
   cd backend
```

2. Crea el entorno virtual e instala dependencias:
```bash
   uv venv --python 3.11
   source .venv/bin/activate  # Mac/Linux
   .venv\Scripts\activate     # Windows
   uv sync
```

3. Crea el archivo `.env` copiando el ejemplo:
```bash
   cp .env.example .env
```
   Edita `.env` y añade tu GROQ_API_KEY.

4. Arranca el servidor:
```bash
   export PYTHONPATH=src
   uvicorn src.app.main:app --reload --port 8000
```

5. Abre la documentación interactiva en:
   http://localhost:8000/docs