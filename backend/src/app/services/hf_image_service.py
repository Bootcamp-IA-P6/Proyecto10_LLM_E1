import httpx
import base64
import os
from app.config import settings


HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"


def generate_image_hf(prompt: str) -> str:
    """
    Genera una imagen con HuggingFace Inference API (FLUX.1-schnell).
    Devuelve URL en formato base64 data URI o cadena vacía si falla.
    """
    if not settings.hf_api_key:
        return ""

    try:
        headers = {"Authorization": f"Bearer {settings.hf_api_key}"}
        payload = {
            "inputs": prompt[:300],
            "parameters": {
                "num_inference_steps": 4,   # schnell es rápido con pocos pasos
                "width":  1024,
                "height": 576,
            }
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(HF_API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                # HF devuelve bytes de la imagen — convertir a base64
                image_bytes  = response.content
                b64_image    = base64.b64encode(image_bytes).decode("utf-8")
                return f"data:image/jpeg;base64,{b64_image}"

            if response.status_code == 503:
                # Modelo cargando — es normal en free tier
                return ""

        return ""

    except Exception:
        return ""