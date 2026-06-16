from langchain_core.prompts import ChatPromptTemplate
from app.agents.state import ContentState
from app.generators.llm_factory import get_llm
from app.services.news_service import get_financial_news


FINANCE_AGENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto en contenido financiero y económico.
Generas contenido preciso, actualizado y adaptado a la plataforma indicada.
Usa las noticias proporcionadas como base factual — no inventes datos.

{company_context}
Idioma de respuesta: {language}"""),
    ("human", """
Tema: {topic}
Plataforma: {platform}
Audiencia: {audience}
Tono: {tone}

Noticias actuales relevantes:
{news_context}

Genera contenido listo para publicar basado en estas noticias reales.
""")
])


def finance_agent_node(state: ContentState) -> ContentState:
    try:
        # Obtener noticias actuales
        news = get_financial_news(state["topic"])

        if news:
            news_context = "\n".join([
                f"- {n['title']}: {n['description']}"
                if isinstance(n, dict)
                else f"- {n}"
                for n in news[:5]
            ])
        else:
            news_context = "No se encontraron noticias recientes sobre este tema."

        llm   = get_llm("groq")
        chain = FINANCE_AGENT_PROMPT | llm

        company_context = (
            f"Contexto de empresa: {state['company_profile']}"
            if state["company_profile"]
            else ""
        )

        response = chain.invoke({
            "topic":           state["topic"],
            "platform":        state["platform"],
            "audience":        state["audience"],
            "tone":            state["tone"],
            "language":        state["language"],
            "news_context":    news_context,
            "company_context": company_context,
        })

        content = response.content if hasattr(response, "content") else str(response)

        return {
            **state,
            "generated_content": content,
            "image_url":         "",
        }

    except Exception as e:
        return {**state, "error": str(e)}