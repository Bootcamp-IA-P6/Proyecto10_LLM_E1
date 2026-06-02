from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.generators.content_generator import generate_content
from app.profile import CompanyProfile, save_profile, get_profile, get_profile_as_text
from app.services.image_service import get_image


app = FastAPI(
    title="Digital Content AI",
    description="Generación automática de contenido con LLMs",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Digital Content AI running"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        # Inyectar perfil de empresa si existe
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

        # Obtener imagen de Unsplash
        image_url = get_image(request.topic)

        return GenerateResponse(
            content=content,
            platform=request.platform,
            model_used=request.model,
            image_url=image_url,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/profile", response_model=CompanyProfile)
def create_profile(profile: CompanyProfile):
    return save_profile(profile)


@app.get("/api/profile", response_model=Optional[CompanyProfile])
def read_profile():
    return get_profile()