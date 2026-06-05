import httpx
from app.config import settings


NEWS_API_URL = "https://newsapi.org/v2/everything"


def get_financial_news(topic: str) -> list[str]:
    """
    Busca noticias financieras actuales sobre el tema dado.
    Devuelve lista de titulares + descripción o lista vacía si falla.
    """
    if not settings.news_api_key:
        return []

    try:
        response = httpx.get(
            NEWS_API_URL,
            params={
                "q": topic,
                "language": "es",
                "sortBy": "publishedAt",
                "pageSize": 5,
            },
            headers={
                "X-Api-Key": settings.news_api_key,
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        news = []
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            if title:
                news.append(f"Titular: {title}\nDescripción: {description}")

        return news

    except Exception:
        return []


def format_news_as_context(news: list[str]) -> str:
    """
    Convierte la lista de noticias en un string de contexto para el prompt.
    """
    if not news:
        return ""
    return "Noticias financieras recientes:\n\n" + "\n\n".join(news)