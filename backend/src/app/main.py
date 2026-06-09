import logging
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.generators.content_generator import generate_content
from app.profile import CompanyProfile, save_profile, get_profile, get_profile_as_text
from app.services.image_service import get_image
from app.services.news_service import get_financial_news, format_news_as_context
from app.services.history_service import save_generation, get_history, delete_generation
from app.rag.arxiv_loader import load_papers
from app.rag.vector_store import build_vector_store
from app.rag.rag_chain import build_rag_chain, run_rag_query
from app.database.database import init_db, get_db
from app.agents.graph import content_graph
from app.agents.state import ContentState

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Digital Content AI",
    description="Generación automática de contenido con LLMs",
    version="3.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Inicialización ────────────────────────────────────────────────

@app.on_event("startup")
def startup_event():
    init_db()


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
    quality_score: Optional[float] = None
    quality_feedback: Optional[str] = None


class ScienceRequest(BaseModel):
    topic: str
    audience: str
    tone: str = "divulgativo"
    language: str = "es"
    max_papers: int = 5


class NewsRequest(BaseModel):
    topic: str
    platform: str
    audience: str
    tone: str = "profesional"
    language: str = "es"


class NewsHeadline(BaseModel):
    title: str
    description: str
    url: str


class FinancialNewsResponse(BaseModel):
    topic: str
    count: int
    news: list[NewsHeadline]


class GenerationResponse(BaseModel):
    id: int
    platform: str
    topic: str
    audience: str
    tone: Optional[str]
    language: Optional[str]
    model_used: str
    content: str
    image_url: Optional[str]
    quality_score: Optional[float] = None
    quality_feedback: Optional[str] = None
    gen_type: str
    created_at: str

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Digital Content AI running"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest, db: Session = Depends(get_db)):
    try:
        company_profile = request.company_profile or get_profile_as_text()

        # Construir estado inicial para el grafo
        initial_state = ContentState(
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            model=request.model,
            company_profile=company_profile,
            content_type="",
            generated_content=None,
            image_url=None,
            quality_score=None,
            quality_feedback=None,
            error=None,
        )

        # Ejecutar el grafo multiagente
        result = content_graph.invoke(initial_state)

        # Comprobar si hubo error en algún agente
        if result.get("error"):
            raise ValueError(result["error"])

        content   = result.get("generated_content", "")
        image_url = result.get("image_url", "")

        save_generation(
            db=db,
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            content=content,
            model_used=request.model,
            tone=request.tone,
            language=request.language,
            image_url=image_url or "",
            gen_type=result.get("content_type", "general"),
            quality_score=result.get("quality_score"),
            quality_feedback=result.get("quality_feedback"),
        )

        return GenerateResponse(
            content=content,
            platform=request.platform,
            model_used=request.model,
            image_url=image_url or "",
            quality_score=result.get("quality_score"),
            quality_feedback=result.get("quality_feedback"),
        )

    except ValueError as e:
        logger.error(f"ValueError en /api/generate: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(f"Error en /api/generate: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/generate/science")
def generate_science(request: ScienceRequest, db: Session = Depends(get_db)):
    try:
        papers = load_papers(
            query=request.topic,
            max_results=request.max_papers,
        )

        if not papers:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron papers sobre: {request.topic}"
            )

        vector_store = build_vector_store(papers)
        chain = build_rag_chain(vector_store)
        query = (
            f"Explica {request.topic} de forma divulgativa "
            f"para {request.audience} en tono {request.tone}. "
            f"Responde en {request.language}."
        )
        content = run_rag_query(chain, query)

        save_generation(
            db=db,
            platform="science",
            topic=request.topic,
            audience=request.audience,
            content=content,
            model_used="ollama+rag",
            tone=request.tone,
            language=request.language,
            gen_type="science",
        )

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
def generate_news(request: NewsRequest, db: Session = Depends(get_db)):
    try:
        news = get_financial_news(request.topic)
        news_context = format_news_as_context(
            [f"Titular: {n['title']}\nDescripción: {n['description']}" for n in news]
        )

        content = generate_content(
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            model="groq",
            company_profile=news_context,
        )

        save_generation(
            db=db,
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            content=content,
            model_used="groq",
            tone=request.tone,
            language=request.language,
            gen_type="news",
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


@app.get("/api/news/financial", response_model=FinancialNewsResponse)
def get_news(topic: str = "bolsa mercados finanzas"):
    try:
        news = get_financial_news(topic)
        return FinancialNewsResponse(
            topic=topic,
            count=len(news),
            news=[NewsHeadline(**item) for item in news],
        )
    except Exception as e:
        logger.exception(f"Error en /api/news/financial: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history", response_model=list[GenerationResponse])
def get_generations(
    limit: int = 20,
    skip: int = 0,
    db: Session = Depends(get_db)
):
    generations = get_history(db, limit=limit, skip=skip)
    return [
        GenerationResponse(
            **{**g.__dict__, "created_at": g.created_at.isoformat()}
        )
        for g in generations
    ]


@app.delete("/api/history/{generation_id}")
def delete_generation_endpoint(
    generation_id: int,
    db: Session = Depends(get_db)
):
    success = delete_generation(db, generation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Generación no encontrada")
    return {"deleted": True}


@app.post("/api/profile", response_model=CompanyProfile)
def create_profile(profile: CompanyProfile):
    return save_profile(profile)


@app.get("/api/profile", response_model=Optional[CompanyProfile])
def read_profile():
    return get_profile()