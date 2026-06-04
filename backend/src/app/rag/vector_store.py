from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


CHROMA_PATH = "./data/chroma_db"
COLLECTION_NAME = "arxiv_papers"

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


def build_vector_store(documents: list[str]) -> Chroma:
    """
    Trocea los documentos, genera embeddings y los persiste en Chroma.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.create_documents(documents)

    return Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )


def load_vector_store() -> Chroma:
    """
    Carga un vector store ya existente desde disco.
    """
    return Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
        collection_name=COLLECTION_NAME,
    )