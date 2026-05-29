from langchain_groq import ChatGroq
from app.config import settings


def get_llm():
    """
    Devuelve una instancia del LLM configurado con Groq.
    """
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=0.7,
    )