from urllib.parse import quote


def generate_image_pollinations(prompt: str) -> str:
    """
    Genera una imagen con IA usando Pollinations.ai.
    No requiere API key. Devuelve URL directa a la imagen.
    """
    try:
        # Limpiar y encodear el prompt
        clean_prompt = prompt.strip()[:200]  # máximo 200 chars
        encoded      = quote(clean_prompt)
        url          = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=720&nologo=true"
        return url

    except Exception:
        return ""