from app.agents.state import ContentState
from app.rag.arxiv_loader import load_papers
from app.rag.vector_store import build_vector_store
from app.rag.rag_chain import build_rag_chain
from app.rag.graph_rag import get_graph_context


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

        # Contexto del grafo de conocimiento (GraphRAG)
        graph_context = get_graph_context(state["topic"], papers)

        # Construir vector store y cadena RAG
        vector_store = build_vector_store(papers)
        chain        = build_rag_chain(vector_store)

        # Query combinando contexto vectorial + grafo
        graph_addition = (
            f"\nContexto adicional del grafo de conocimiento:\n{graph_context}"
            if graph_context
            else ""
        )

        query = (
            f"Explica {state['topic']} de forma divulgativa "
            f"para {state['audience']} con tono {state['tone']}. "
            f"Responde en {state['language']}."
            f"{graph_addition}"
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