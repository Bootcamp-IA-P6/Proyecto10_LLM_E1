from huggingface_hub import InferenceClient
import base64
import io

from app.config import settings


def generate_image_hf(prompt: str) -> str:
    """
    Genera una imagen con Hugging Face FLUX.1-schnell.
    Devuelve una data URI base64 o cadena vacía si falla.
    """

    print(f"HF_API_KEY presente: {bool(settings.hf_api_key)}")

    if not settings.hf_api_key:
        return ""

    try:
        client = InferenceClient(
            api_key=settings.hf_api_key
        )

        image = client.text_to_image(
            prompt[:300],
            model="black-forest-labs/FLUX.1-schnell",
            width=1024,
            height=576,
        )

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")

        b64_image = base64.b64encode(
            buffer.getvalue()
        ).decode("utf-8")

        return f"data:image/jpeg;base64,{b64_image}"

    except Exception as e:
        print(f"Error en HF: {e}")
        return ""