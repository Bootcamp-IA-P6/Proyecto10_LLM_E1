from app.agents.state import ContentState
from app.rag.arxiv_loader import load_papers
from app.rag.vector_store import build_vector_store
from app.rag.rag_chain import build_rag_chain


def science_agent_node(state: ContentState) -> ContentState:
    try:
        # Cargar papers de arXiv
        papers = load_papers(
            query=state["topic"],
            max_results=3,
        )

        if not papers:
            return {
                **state,
                "error": "No se encontraron papers para este topic. Prueba en inglés.",
            }

        # Construir vector store con los papers
        vector_store = build_vector_store(papers)

        # Construir cadena RAG con Ollama
        chain = build_rag_chain(vector_store)

        # Query en el idioma del usuario
        query = (
            f"Explica {state['topic']} de forma divulgativa "
            f"para {state['audience']} con tono {state['tone']}. "
            f"Responde en {state['language']}."
        )

        result = chain.invoke({"query": query})

        content = (
            result["result"]
            if isinstance(result, dict) and "result" in result
            else str(result)
        )

        return {
            **state,
            "generated_content": content,
            "image_url":         "",
        }

    except Exception as e:
        return {**state, "error": str(e)}