import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.generators.content_generator import generate_content
from app.profile import CompanyProfile, save_profile, get_profile, get_profile_as_text
from app.services.image_service import get_image
from app.services.news_service import get_financial_news, format_news_as_context
from app.rag.arxiv_loader import load_papers
from app.rag.vector_store import build_vector_store, load_vector_store
from app.rag.rag_chain import build_rag_chain, run_rag_query

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Digital Content AI",
    description="Generación automática de contenido con LLMs",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Modelos Pydantic ──────────────────────────────────────────────

class GenerateRequest(BaseModel):
    platform: str
    topic: str
    audience: str
    tone: str = "profesional"
    language: str = "es"
    model: str = "groq"
    company_profile: Optional[str] = ""


class GenerateResponse(BaseModel):
    content: str
    platform: str
    model_used: str
    image_url: str = ""


class ScienceRequest(BaseModel):
    topic: str
    audience: str
    tone: str = "divulgativo"
    language: str = "es"
    max_papers: int = 10


class NewsRequest(BaseModel):
    topic: str
    platform: str
    audience: str
    tone: str = "profesional"
    language: str = "es"


# ── Endpoints ─────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Digital Content AI running"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        company_profile = request.company_profile or get_profile_as_text()

        content = generate_content(
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            model=request.model,
            company_profile=company_profile,
        )

        image_url = get_image(request.topic)

        return GenerateResponse(
            content=content,
            platform=request.platform,
            model_used=request.model,
            image_url=image_url,
        )
    except ValueError as e:
        logger.error(f"ValueError en /api/generate: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error en /api/generate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/science")
def generate_science(request: ScienceRequest):
    try:
        # 1. Descargar papers de arXiv
        papers = load_papers(
            query=request.topic,
            max_results=request.max_papers,
        )

        if not papers:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron papers sobre: {request.topic}"
            )

        # 2. Construir vector store con los papers
        vector_store = build_vector_store(papers)

        # 3. Construir cadena RAG y ejecutar query
        chain = build_rag_chain(vector_store)
        query = (
            f"Explica {request.topic} de forma divulgativa "
            f"para {request.audience} en tono {request.tone}. "
            f"Responde en {request.language}."
        )
        content = run_rag_query(chain, query)

        return {
            "content": content,
            "topic": request.topic,
            "papers_used": len(papers),
            "model_used": "ollama+rag",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error en /api/generate/science: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate/news")
def generate_news(request: NewsRequest):
    try:
        # 1. Obtener noticias actuales
        news = get_financial_news(request.topic)
        news_context = format_news_as_context(news)

        # 2. Generar contenido inyectando noticias como contexto
        content = generate_content(
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            model="groq",
            company_profile=news_context,
        )

        return {
            "content": content,
            "topic": request.topic,
            "platform": request.platform,
            "news_count": len(news),
            "model_used": "groq",
        }
    except Exception as e:
        logger.exception(f"Error en /api/generate/news: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/financial")
def get_news(topic: str = "bolsa mercados finanzas"):
    try:
        news = get_financial_news(topic)
        return {
            "topic": topic,
            "count": len(news),
            "news": news,
        }
    except Exception as e:
        logger.exception(f"Error en /api/news/financial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile", response_model=CompanyProfile)
def create_profile(profile: CompanyProfile):
    return save_profile(profile)


@app.get("/api/profile", response_model=Optional[CompanyProfile])
def read_profile():
    return get_profile()