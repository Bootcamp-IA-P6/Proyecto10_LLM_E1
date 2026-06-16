# Digital Content AI

Sistema de generación automática de contenido para múltiples plataformas y audiencias, impulsado por modelos de lenguaje de gran escala (LLMs).

Genera contenido listo para publicar en **Blog, Twitter/X, LinkedIn e Instagram** a partir de un tema, audiencia, tono e idioma. Incluye generación de contenido científico divulgativo con RAG sobre papers de arXiv y contenido financiero con noticias en tiempo real.

Construido con FastAPI, LangChain, Groq, Ollama y Next.js.

---

## Estructura del repositorio

```
digital-content-ai/
├── backend/          # API REST con FastAPI + LangChain + Groq + Ollama
├── frontend/         # Interfaz web con Next.js 15 + TypeScript
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Requisitos previos

- Python 3.11+
- Node.js 20+
- uv (`pip install uv`)
- Ollama instalado — [ollama.com/download](https://ollama.com/download)
- API Key de Groq — [console.groq.com](https://console.groq.com) (gratuita, sin tarjeta)
- API Key de Unsplash — [unsplash.com/developers](https://unsplash.com/developers) (gratuita)
- API Key de NewsAPI — [newsapi.org](https://newsapi.org) (gratuita, 100 req/día)
- API Key de LangSmith — [smith.langchain.com](https://smith.langchain.com) (gratuita, 5000 trazas/mes)

---

## Arranque rápido

### 1. Backend

```bash
cd backend
uv venv --python 3.11
source .venv/bin/activate     # Mac/Linux
.venv\Scripts\activate        # Windows
uv sync
cp .env.example .env
# Editar .env y añadir las keys necesarias
```

**Mac/Linux:**
```bash
export PYTHONPATH=src
uvicorn src.app.main:app --reload --port 8000
```

**Windows (Git Bash):**
```bash
PYTHONPATH=src uvicorn src.app.main:app --reload --port 8000
```

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH="src"; uvicorn src.app.main:app --reload --port 8000
```

API disponible en `http://localhost:8000`
Documentación interactiva en `http://localhost:8000/docs`

⚠️ La primera vez que arranca descarga el modelo de embeddings `all-MiniLM-L6-v2` (~90MB).

### 2. Ollama (necesario para RAG científico)

```bash
ollama pull llama3.2
```

Ollama arranca automáticamente al instalar. Corre en `http://localhost:11434`.

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Aplicación disponible en `http://localhost:3000`

### 4. Con Docker (arranque completo)

```bash
docker compose up --build
```

Levanta backend en `localhost:8000` y frontend en `localhost:3000`.

---

## Variables de entorno

### backend/.env

```bash
# Groq
GROQ_API_KEY=tu_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Unsplash
UNSPLASH_ACCESS_KEY=tu_unsplash_key

# LangSmith
LANGCHAIN_API_KEY=tu_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=digital-content-ai

# NewsAPI
NEWS_API_KEY=tu_newsapi_key
```

### frontend/.env.local

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## API

### `POST /api/generate`
Genera contenido para la plataforma indicada.

```json
{
  "platform": "twitter",
  "topic": "inteligencia artificial en educación",
  "audience": "profesores de secundaria",
  "tone": "divulgativo",
  "language": "es",
  "model": "groq"
}
```

| Campo | Tipo | Obligatorio | Valores |
|-------|------|-------------|---------|
| `platform` | string | ✅ | `blog` `twitter` `linkedin` `instagram` |
| `topic` | string | ✅ | texto libre |
| `audience` | string | ✅ | texto libre |
| `tone` | string | ❌ | default: `profesional` |
| `language` | string | ❌ | `es` `en` `fr` `it` |
| `model` | string | ❌ | `groq` (default) `ollama` |

### `POST /api/generate/science`
Genera contenido científico divulgativo con RAG sobre papers de arXiv.

```json
{
  "topic": "artificial intelligence",
  "audience": "público general",
  "tone": "divulgativo",
  "language": "es",
  "max_papers": 3
}
```

⚠️ Topics en inglés dan mejores resultados. Puede tardar 2-3 minutos.

### `POST /api/generate/news`
Genera contenido financiero con noticias reales de NewsAPI.

```json
{
  "topic": "bolsa española",
  "platform": "linkedin",
  "audience": "inversores",
  "tone": "profesional",
  "language": "es"
}
```

### `GET /api/news/financial`
Devuelve titulares financieros actuales. Query param opcional: `?topic=bolsa`

### `POST /api/profile`
Guarda el perfil de empresa en memoria.

### `GET /api/profile`
Devuelve el perfil de empresa guardado.

### `GET /api/history`
Devuelve el historial de generaciones. Params: `?limit=20&skip=0`

### `DELETE /api/history/{id}`
Elimina una generación del historial.

### `GET /`
Health check.

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI · Uvicorn · Python 3.11 |
| LLM framework | LangChain · LangGraph |
| LLMs | Groq (llama-3.3-70b) · Ollama (llama3.2) |
| RAG | LangChain RAG · Chroma · sentence-transformers · arXiv |
| Trazabilidad | LangSmith |
| Base de datos | SQLite + SQLAlchemy |
| Frontend | Next.js 15 · TypeScript · Tailwind CSS v4 |
| Imágenes | Unsplash API |
| Noticias | NewsAPI |
| Contenedores | Docker · docker-compose |
| Gestión deps backend | uv |
| Gestión deps frontend | npm |

---

## Fases del proyecto

| Fase | Estado | Descripción |
|------|--------|-------------|
| Fase 1 — Esencial | ✅ Completada | FastAPI + prompts + Groq + UI Next.js |
| Fase 2 — Medio | ✅ Completada | Ollama + Docker + imágenes + perfil empresa |
| Fase 3 — Avanzado | ✅ Completada | RAG arXiv + Chroma + LangSmith + noticias + historial SQLite |
| Fase 4 — Experto | ✅ Completada | LangGraph multiagente + GraphRAG + guardarraíles + quality score UI |


---

## Ramas Git

```
main                    ← producción estable (protegida, solo PR)
develop                 ← integración
feat/fase-1-backend
feat/fase-1-frontend
feat/fase-2-backend
feat/fase-2-frontend
feat/fase-3-backend
feat/fase-3-frontend
feat/fase-4-backend
feat/fase-4-frontend
```

---

## Equipo

Proyecto desarrollado como prueba de concepto para **Digital Content**
en el marco del bootcamp de IA de Factoria F5.