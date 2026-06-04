from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from app.generators.llm_factory import get_llm


def build_rag_chain(vector_store: Chroma) -> RetrievalQA:
    """
    Construye la cadena RAG con Ollama como LLM y Chroma como retriever.
    """
    llm = get_llm("ollama")
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )


def run_rag_query(chain: RetrievalQA, query: str) -> str:
    """
    Ejecuta una query sobre la cadena RAG y devuelve el resultado como string.
    """
    result = chain.invoke({"query": query})
    return result["result"]