import json
import re
from app.agents.state import ContentState
from app.generators.llm_factory import get_llm


QUALITY_PROMPT = """Eres un evaluador de calidad de contenido para redes sociales y blogs.

Evalúa el siguiente contenido generado para la plataforma "{platform}":

---
{content}
---

Criterios de evaluación:
1. Coherencia: el texto tiene sentido y fluye bien
2. Adecuación: el formato y tono son correctos para {platform}
3. Veracidad: no hay afirmaciones claramente falsas o inventadas
4. Completitud: el contenido está completo y no se corta a mitad

Responde ÚNICAMENTE con un JSON válido, sin texto adicional:
{{"score": 0.0, "feedback": "razón breve en una frase"}}

El score debe ser entre 0.0 y 1.0:
- 0.8 a 1.0: contenido de alta calidad
- 0.6 a 0.8: contenido aceptable con pequeños problemas
- 0.0 a 0.6: contenido con problemas importantes que requiere revisión
"""


def quality_check_node(state: ContentState) -> ContentState:
    # Si no hay contenido generado o hay error previo no evaluar
    if not state.get("generated_content") or state.get("error"):
        return {
            **state,
            "quality_score":    0.0,
            "quality_feedback": "No se pudo evaluar — sin contenido generado",
        }

    try:
        llm    = get_llm("groq")
        prompt = QUALITY_PROMPT.format(
            platform=state["platform"],
            content=state["generated_content"][:2000],  # limitar tokens
        )

        response = llm.invoke(prompt)
        text     = response.content if hasattr(response, "content") else str(response)

        # Extraer JSON de la respuesta
        json_match = re.search(r'\{.*?\}', text, re.DOTALL)
        if json_match:
            data     = json.loads(json_match.group())
            score    = float(data.get("score", 0.7))
            feedback = str(data.get("feedback", "Evaluación completada"))
        else:
            score    = 0.7
            feedback = "Evaluación completada"

        return {
            **state,
            "quality_score":    round(score, 2),
            "quality_feedback": feedback,
        }

    except Exception as e:
        # Si falla la evaluación no bloqueamos la respuesta
        return {
            **state,
            "quality_score":    0.7,
            "quality_feedback": f"Evaluación no disponible: {str(e)}",
        }