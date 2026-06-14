import pytest


class TestHealthCheck:
    def test_health_check(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestGenerateEndpoint:

    def test_generate_blog(self, client):
        response = client.post("/api/generate", json={
            "platform": "blog",
            "topic":    "inteligencia artificial en educación",
            "audience": "profesores",
            "tone":     "divulgativo",
            "language": "es",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 100
        assert data["platform"] == "blog"
        assert data["model_used"] == "groq"

    def test_generate_twitter(self, client):
        response = client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "tendencias tecnológicas",
            "audience": "profesionales",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 50
        assert data["platform"] == "twitter"

    def test_generate_linkedin(self, client):
        response = client.post("/api/generate", json={
            "platform": "linkedin",
            "topic":    "liderazgo empresarial",
            "audience": "directivos",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert data["platform"] == "linkedin"

    def test_generate_instagram(self, client):
        response = client.post("/api/generate", json={
            "platform": "instagram",
            "topic":    "viajes sostenibles",
            "audience": "millennials",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert data["platform"] == "instagram"

    def test_generate_returns_quality_score(self, client):
        response = client.post("/api/generate", json={
            "platform": "blog",
            "topic":    "tecnología blockchain",
            "audience": "inversores",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "quality_score" in data
        assert "quality_feedback" in data
        assert data["quality_score"] is not None
        assert 0.0 <= data["quality_score"] <= 1.0

    def test_generate_with_english_language(self, client):
        response = client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "artificial intelligence trends",
            "audience": "tech professionals",
            "language": "en",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 50

    def test_generate_with_image_unsplash(self, client):
        response = client.post("/api/generate", json={
            "platform":     "blog",
            "topic":        "naturaleza y medio ambiente",
            "audience":     "ecologistas",
            "model":        "groq",
            "image_source": "unsplash",
        })
        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data

    def test_generate_with_image_pollinations(self, client):
        response = client.post("/api/generate", json={
            "platform":     "blog",
            "topic":        "ciudades del futuro",
            "audience":     "urbanistas",
            "model":        "groq",
            "image_source": "pollinations",
        })
        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data
        assert "pollinations.ai" in data["image_url"]

    def test_generate_missing_platform(self, client):
        response = client.post("/api/generate", json={
            "topic":    "tecnología",
            "audience": "general",
        })
        assert response.status_code == 422  # Validation error

    def test_generate_missing_topic(self, client):
        response = client.post("/api/generate", json={
            "platform": "blog",
            "audience": "general",
        })
        assert response.status_code == 422

    def test_generate_invalid_model(self, client):
        response = client.post("/api/generate", json={
            "platform": "blog",
            "topic":    "tecnología",
            "audience": "general",
            "model":    "modelo_inexistente",
        })
        assert response.status_code in [400, 500]

    def test_generate_with_company_profile(self, client):
        response = client.post("/api/generate", json={
            "platform":        "linkedin",
            "topic":           "innovación empresarial",
            "audience":        "clientes",
            "model":           "groq",
            "company_profile": "TechCorp: empresa tecnológica innovadora",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 50

    def test_generate_saves_to_history(self, client):
        # Generar contenido
        client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "test historial automatico",
            "audience": "testers",
            "model":    "groq",
        })
        # Verificar que se guardó en historial
        history = client.get("/api/history").json()
        topics  = [h["topic"] for h in history]
        assert "test historial automatico" in topics