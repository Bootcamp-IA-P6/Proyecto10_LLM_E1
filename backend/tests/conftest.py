import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# ==========================================================
# TEST DATABASE
# ==========================================================

TEST_DB_FILE = tempfile.mktemp(suffix=".db")
TEST_DATABASE_URL = f"sqlite:///{TEST_DB_FILE}"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================================
# MOCK DATA
# ==========================================================

MOCK_GENERATED_CONTENT = """
Contenido de prueba generado automáticamente para testing.

Este texto tiene longitud suficiente para superar todos los
asserts de los tests sin necesidad de llamar a Groq,
LangChain ni ningún proveedor externo.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
"""


MOCK_GRAPH_RESULT = {
    "platform": "blog",
    "topic": "test topic",
    "audience": "testers",
    "tone": "profesional",
    "language": "es",
    "model": "groq",
    "company_profile": "",
    "content_type": "social",
    "generated_content": MOCK_GENERATED_CONTENT,
    "image_url": "https://unsplash.com/test.jpg",
    "quality_score": 0.8,
    "quality_feedback": "Contenido coherente y adecuado.",
    "error": None,
}


MOCK_NEWS = [
    {
        "title": "Noticia test",
        "description": "Descripción de prueba",
        "url": "https://test.com",
    }
]


# ==========================================================
# HELPERS
# ==========================================================

def fake_image_by_source(topic, source):
    if source == "pollinations":
        return "https://image.pollinations.ai/prompt/test"

    return "https://unsplash.com/test.jpg"


def fake_graph_invoke(state):
    return MOCK_GRAPH_RESULT


# ==========================================================
# CLIENT FIXTURE
# ==========================================================

@pytest.fixture(scope="session")
def client():

    with patch(
        "app.database.database.DATABASE_URL",
        TEST_DATABASE_URL,
    ), patch(
        "app.database.database.engine",
        engine,
    ):

        from app.database.models import Base

        Base.metadata.create_all(bind=engine)

        from app.main import app
        from app.database.database import get_db

        app.dependency_overrides[get_db] = override_get_db

        fake_vector_store = MagicMock()

        fake_chain = MagicMock()
        fake_chain.invoke.return_value = MOCK_GENERATED_CONTENT

        with (

            # ==================================================
            # GRAPH AGENT (IMPORTANTE)
            # ==================================================
            patch("app.main.content_graph") as mock_graph,

            # ==================================================
            # GENERACIÓN DE CONTENIDO
            # ==================================================
            patch(
                "app.main.generate_content",
                return_value=MOCK_GENERATED_CONTENT,
            ),

            # ==================================================
            # NEWS
            # ==================================================
            patch(
                "app.main.get_financial_news",
                return_value=MOCK_NEWS,
            ),

            patch(
                "app.main.format_news_as_context",
                return_value="Contexto financiero mockeado",
            ),

            # ==================================================
            # IMÁGENES
            # ==================================================
            patch(
                "app.main.get_image",
                return_value="https://unsplash.com/test.jpg",
            ),

            patch(
                "app.main.get_image_by_source",
                side_effect=fake_image_by_source,
            ),

            patch(
                "app.services.image_service.get_image",
                return_value="https://unsplash.com/test.jpg",
            ),

            patch(
                "app.services.pollinations_service.generate_image_pollinations",
                return_value="https://image.pollinations.ai/prompt/test",
            ),

            # ==================================================
            # RAG
            # ==================================================
            patch(
                "app.main.load_papers",
                return_value=[
                    """
                    Título: Test Paper

                    Resumen:
                    Paper de prueba sobre IA.
                    """
                ],
            ),

            patch(
                "app.main.build_vector_store",
                return_value=fake_vector_store,
            ),

            patch(
                "app.main.build_rag_chain",
                return_value=fake_chain,
            ),

            patch(
                "app.main.run_rag_query",
                return_value=MOCK_GENERATED_CONTENT,
            ),

            # ==================================================
            # PATCHES DIRECTOS DE MÓDULOS RAG
            # ==================================================
            patch(
                "app.rag.arxiv_loader.load_papers",
                return_value=[
                    """
                    Título: Test Paper

                    Resumen:
                    Paper de prueba sobre IA.
                    """
                ],
            ),

            patch(
                "app.rag.vector_store.build_vector_store",
                return_value=fake_vector_store,
            ),

            patch(
                "app.rag.rag_chain.build_rag_chain",
                return_value=fake_chain,
            ),

            patch(
                "app.rag.rag_chain.run_rag_query",
                return_value=MOCK_GENERATED_CONTENT,
            ),
        ):

            # IMPORTANTE
            mock_graph.invoke.side_effect = fake_graph_invoke

            with TestClient(app) as c:
                yield c

        app.dependency_overrides.clear()

        try:
            Base.metadata.drop_all(bind=engine)
        except Exception:
            pass

        try:
            if os.path.exists(TEST_DB_FILE):
                os.remove(TEST_DB_FILE)
        except PermissionError:
            pass