import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Groq
    groq_api_key: str
    groq_model: str = "llama-3.3-70b-versatile"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # Unsplash
    unsplash_access_key: str = ""

    # LangSmith
    langchain_api_key: str = ""
    langchain_tracing_v2: bool = False
    langchain_project: str = "digital-content-ai"

    # NewsAPI
    news_api_key: str = ""

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()

# Configurar LangSmith en variables de entorno del sistema
# LangChain las lee directamente desde os.environ, no desde settings
if settings.langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
    os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project