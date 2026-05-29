from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from app.generators.content_generator import generate_content


app = FastAPI(
    title="Digital Content AI",
    description="Generación automática de contenido con LLMs",
    version="1.0.0",
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
    company_profile: Optional[str] = ""


class GenerateResponse(BaseModel):
    content: str
    platform: str
    model_used: str


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Digital Content AI running"}


@app.post("/api/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    try:
        content = generate_content(
            platform=request.platform,
            topic=request.topic,
            audience=request.audience,
            tone=request.tone,
            language=request.language,
            company_profile=request.company_profile,
        )
        return GenerateResponse(
            content=content,
            platform=request.platform,
            model_used="llama-3.3-70b-versatile",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))