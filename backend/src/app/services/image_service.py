import httpx
from app.config import settings


UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"


def get_image(topic: str) -> str:
    """
    Busca una imagen relevante en Unsplash para el tema dado.
    Devuelve la URL de la primera imagen o cadena vacía si falla.
    """
    if not settings.unsplash_access_key:
        return ""

    try:
        response = httpx.get(
            UNSPLASH_API_URL,
            params={
                "query": topic,
                "per_page": 1,
                "orientation": "landscape",
            },
            headers={
                "Authorization": f"Client-ID {settings.unsplash_access_key}"
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if results:
            return results[0]["urls"]["regular"]
        return ""

    except Exception:
        return ""