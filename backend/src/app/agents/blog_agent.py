from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import ContentState
from app.generators.llm_factory import get_llm
from app.services.image_service import get_image


BLOG_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto redactor de contenido para blogs con 
conocimientos avanzados de SEO y marketing de contenidos.
Escribe posts atractivos, bien estructurados y optimizados para SEO.

Estructura obligatoria:
- Título principal con H1
- Introducción enganchadora (2-3 párrafos)
- Al menos 3 secciones con subtítulos H2
- Conclusión con llamada a la acción
- Longitud mínima: 500 palabras

{company_context}
Idioma de respuesta: {language}"""),
    ("human", """
Tema: {topic}
Audiencia: {audience}
Tono: {tone}

Genera el post completo listo para publicar.
""")
])


def blog_agent_node(state: ContentState) -> ContentState:
    try:
        llm   = get_llm("groq")
        chain = BLOG_AGENT_PROMPT | llm

        company_context = (
            f"Contexto de empresa: {state['company_profile']}"
            if state["company_profile"]
            else ""
        )

        response = chain.invoke({
            "topic":           state["topic"],
            "audience":        state["audience"],
            "tone":            state["tone"],
            "language":        state["language"],
            "company_context": company_context,
        })

        content   = response.content if hasattr(response, "content") else str(response)
        image_url = get_image(state["topic"])

        return {
            **state,
            "generated_content": content,
            "image_url":         image_url,
        }

    except Exception as e:
        return {**state, "error": str(e)}