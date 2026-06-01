# Digital Content AI

Sistema de generación automática de contenido para múltiples plataformas y audiencias, impulsado por modelos de lenguaje de gran escala (LLMs).

Genera contenido listo para publicar en **Blog, Twitter/X, LinkedIn e Instagram** a partir de un tema, audiencia, tono e idioma. Construido con FastAPI, LangChain, Groq y Next.js.

---

## Estructura del repositorio

```
digital-content-ai/
├── backend/          # API REST con FastAPI + LangChain + Groq
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
- API Key de Groq — [console.groq.com](https://console.groq.com) (gratuita, sin tarjeta)

---

## Arranque rápido

### 1. Backend

```bash
cd backend
uv venv --python 3.11
source .venv/bin/activate   # Mac/Linux
source .venv\Scripts\activate      # Windows
uv sync
cp .env.example .env
# Editar .env y añadir GROQ_API_KEY
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

---

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
# .env.local ya apunta a http://localhost:8000 por defecto
npm run dev
```

Aplicación disponible en `http://localhost:3000`

---

## Variables de entorno

### backend/.env

```bash
GROQ_API_KEY=tu_api_key_aqui
GROQ_MODEL=llama-3.3-70b-versatile
```

### frontend/.env.local

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## API

### `POST /api/generate`

Genera contenido para la plataforma indicada.

**Body:**
```json
{
  "platform": "twitter",
  "topic": "inteligencia artificial en educación",
  "audience": "profesores de secundaria",
  "tone": "divulgativo",
  "language": "es",
  "company_profile": ""
}
```

| Campo | Tipo | Obligatorio | Valores |
|-------|------|-------------|---------|
| `platform` | string | ✅ | `blog` `twitter` `linkedin` `instagram` |
| `topic` | string | ✅ | texto libre |
| `audience` | string | ✅ | texto libre |
| `tone` | string | ❌ | default: `profesional` |
| `language` | string | ❌ | `es` `en` `fr` `it` |
| `company_profile` | string | ❌ | default: vacío |

**Respuesta:**
```json
{
  "content": "contenido generado...",
  "platform": "twitter",
  "model_used": "llama-3.3-70b-versatile"
}
```

### `GET /`

Health check. Devuelve `{"status": "ok"}`.

---

## Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Backend | FastAPI · Uvicorn · Python 3.11 |
| LLM framework | LangChain |
| LLM | Groq — llama-3.3-70b-versatile |
| Frontend | Next.js 15 · TypeScript · Tailwind CSS v4 |
| Gestión deps backend | uv |
| Gestión deps frontend | npm |

---

## Fases del proyecto

| Fase | Estado | Descripción |
|------|--------|-------------|
| Fase 1 — Esencial | ✅ En progreso | FastAPI + prompts + Groq + UI Next.js |
| Fase 2 — Medio | 🔲 Pendiente | Ollama + Docker + imágenes + perfil empresa |
| Fase 3 — Avanzado | 🔲 Pendiente | RAG arXiv + LangSmith + multiidioma + noticias |
| Fase 4 — Experto | 🔲 Pendiente | LangGraph multiagente + GraphRAG + guardarraíles |

---

## Ramas Git

```
main              ← producción estable (protegida, solo PR)
develop           ← integración
feat/fase-1-backend
feat/fase-1-frontend
feat/fase-2-ollama
feat/fase-3-rag
feat/fase-4-agents
```

---

## Equipo

Proyecto desarrollado como prueba de concepto para **Digital Content** en el marco del bootcamp de IA de Factoria F5.