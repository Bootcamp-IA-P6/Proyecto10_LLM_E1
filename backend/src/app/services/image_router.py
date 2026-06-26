from app.services.image_service import get_image
from app.services.hf_image_service import generate_image_hf
from app.services.pollinations_service import generate_image_pollinations


def get_image_by_source(topic: str, source: str = "unsplash") -> str:
    """
    Devuelve una imagen según la fuente seleccionada.

    source:
        "unsplash"      → Unsplash API (foto real)
        "huggingface"   → HuggingFace FLUX.1 (imagen generada con IA)
        "pollinations"  → Pollinations.ai (imagen generada con IA, sin key)
    """
    if source == "huggingface":
        url = generate_image_hf(topic)
        # Fallback a pollinations si HF falla
        if not url:
            url = generate_image_pollinations(topic)
        return url

    if source == "pollinations":
        return generate_image_pollinations(topic)

    # Default → Unsplash
    return get_image(topic)