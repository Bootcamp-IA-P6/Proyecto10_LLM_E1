import httpx
from app.config import settings


NEWS_API_URL = "https://newsapi.org/v2/everything"


def get_financial_news(topic: str) -> list[dict]:
    """
    Busca noticias financieras actuales sobre el tema dado.
    Devuelve lista de dicts con title, description y url.
    Devuelve lista vacía si falla silenciosamente.
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
            url = article.get("url", "")
            if title:
                news.append({
                    "title": title,
                    "description": description,
                    "url": url,
                })

        return news

    except Exception:
        return []


def format_news_as_context(news: list[str]) -> str:
    """
    Convierte la lista de strings de noticias en contexto para el prompt.
    """
    if not news:
        return ""
    return "Noticias financieras recientes:\n\n" + "\n\n".join(news)