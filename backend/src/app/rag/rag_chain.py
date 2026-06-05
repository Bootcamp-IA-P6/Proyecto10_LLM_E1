from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.generators.llm_factory import get_llm


RAG_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Eres un divulgador científico experto.
Usa el siguiente contexto de papers científicos para responder.
Si el contexto no es suficiente, indícalo claramente.

Contexto:
{context}"""),
    ("human", "{question}"),
])


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vector_store: Chroma):
    """
    Construye la cadena RAG con Ollama como LLM y Chroma como retriever.
    """
    llm = get_llm("ollama")
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain


def run_rag_query(chain, query: str) -> str:
    """
    Ejecuta una query sobre la cadena RAG y devuelve el resultado como string.
    """
    return chain.invoke(query)