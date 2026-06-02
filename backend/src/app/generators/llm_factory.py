from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM
from app.config import settings


def get_llm(model: str = "groq"):
    """
    Devuelve el LLM correspondiente según el parámetro recibido.
    - 'groq'   → ChatGroq (online, API de Groq)
    - 'ollama' → OllamaLLM (local, sin límites)
    """
    if model == "groq":
        return ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.7,
        )
    elif model == "ollama":
        return OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
        )
    else:
        raise ValueError(f"Modelo no soportado: {model}. Usa 'groq' o 'ollama'.")