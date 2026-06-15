import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

TEST_DB_FILE = tempfile.mktemp(suffix=".db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

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


@pytest.fixture(scope="session")
def client():
    # Importar aquí para que los patches se apliquen antes
    with patch("app.database.database.DATABASE_URL", TEST_DATABASE_URL), \
         patch("app.database.database.engine", engine):

        from app.database.models import Base
        Base.metadata.create_all(bind=engine)

        from app.main import app
        from app.database.database import get_db

        app.dependency_overrides[get_db] = override_get_db

        with patch("app.agents.graph.content_graph") as mock_graph, \
             patch("app.services.image_service.get_image",
                   return_value="https://unsplash.com/test.jpg"), \
             patch("app.services.pollinations_service.generate_image_pollinations",
                   return_value="https://image.pollinations.ai/prompt/test"), \
             patch("app.services.news_service.get_financial_news",
                   return_value=[{"title": "Noticia test", "description": "Desc test", "url": "https://test.com"}]), \
             patch("app.rag.arxiv_loader.load_papers",
                   return_value=["Título: Test Paper\nResumen: Paper de prueba sobre IA."]), \
             patch("app.rag.vector_store.build_vector_store", return_value=MagicMock()), \
             patch("app.rag.rag_chain.build_rag_chain", return_value=MagicMock()), \
             patch("app.rag.rag_chain.run_rag_query",
                   return_value="Contenido científico de prueba generado por RAG."):

            mock_graph.invoke.return_value = MOCK_GRAPH_RESULT

            with TestClient(app) as c:
                yield c

        app.dependency_overrides.clear()

    # Limpiar fichero temporal
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)