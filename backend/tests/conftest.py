import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.database import get_db
from app.database.models import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# Mock del grafo LangGraph para no llamar a Groq/Ollama en tests
MOCK_GRAPH_RESULT = {
    "platform":          "blog",
    "topic":             "test topic",
    "audience":          "testers",
    "tone":              "profesional",
    "language":          "es",
    "model":             "groq",
    "company_profile":   "",
    "content_type":      "social",
    "generated_content": "Contenido de prueba generado automáticamente para el test.",
    "image_url":         "",
    "quality_score":     0.8,
    "quality_feedback":  "Contenido coherente y adecuado.",
    "error":             None,
}


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[get_db] = override_get_db

    with patch("app.agents.graph.content_graph") as mock_graph, \
         patch("app.services.image_service.get_image", return_value="https://unsplash.com/test.jpg"), \
         patch("app.services.pollinations_service.generate_image_pollinations",
               return_value="https://image.pollinations.ai/prompt/test"), \
         patch("app.services.news_service.get_financial_news",
               return_value=[{"title": "Noticia test", "description": "Descripción test", "url": "https://test.com"}]), \
         patch("app.rag.arxiv_loader.load_papers",
               return_value=["Título: Test Paper\nResumen: Este es un paper de prueba sobre IA."]), \
         patch("app.rag.vector_store.build_vector_store") as mock_vs, \
         patch("app.rag.rag_chain.build_rag_chain") as mock_chain, \
         patch("app.rag.rag_chain.run_rag_query",
               return_value="Contenido científico de prueba generado por RAG."):

        # Configurar mock del grafo
        mock_graph.invoke.return_value = MOCK_GRAPH_RESULT

        # Configurar mock de la cadena RAG
        mock_chain_instance       = MagicMock()
        mock_chain_instance.invoke.return_value = "Contenido RAG de prueba."
        mock_chain.return_value   = mock_chain_instance
        mock_vs.return_value      = MagicMock()

        with TestClient(app) as c:
            yield c

    app.dependency_overrides.clear()