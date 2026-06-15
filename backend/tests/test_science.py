import pytest


class TestScienceEndpoints:

    def test_generate_science_basic(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "artificial intelligence",
            "audience": "público general",
            "tone":     "divulgativo",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content"    in data
        assert "model_used" in data
        assert len(data["content"]) > 100

    def test_generate_science_returns_papers_used(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "machine learning",
            "audience": "estudiantes",
            "tone":     "educativo",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "papers_used" in data
        assert data["papers_used"] > 0

    def test_generate_science_returns_image_url(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "neural networks",
            "audience": "universitarios",
            "tone":     "educativo",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data

    def test_generate_science_model_used(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "quantum computing",
            "audience": "público general",
            "tone":     "divulgativo",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["model_used"] == "ollama+rag"

    def test_generate_science_in_english(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "deep learning",
            "audience": "general public",
            "tone":     "educational",
            "language": "en",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 100

    def test_generate_science_max_papers(self, client):
        response = client.post("/api/generate/science", json={
            "topic":      "robotics",
            "audience":   "estudiantes",
            "tone":       "educativo",
            "language":   "es",
            "max_papers": 2,
        })
        assert response.status_code == 200
        data = response.json()
        assert data["papers_used"] <= 2

    def test_generate_science_saves_to_history(self, client):
        client.post("/api/generate/science", json={
            "topic":    "test science history",
            "audience": "testers",
            "tone":     "divulgativo",
            "language": "es",
        })
        history = client.get("/api/history").json()
        topics  = [h["topic"] for h in history]
        assert "test science history" in topics

    def test_generate_science_gen_type(self, client):
        client.post("/api/generate/science", json={
            "topic":    "test gen type science",
            "audience": "testers",
            "tone":     "divulgativo",
            "language": "es",
        })
        history   = client.get("/api/history").json()
        gen_types = [h["gen_type"] for h in history
                     if h["topic"] == "test gen type science"]
        assert len(gen_types) > 0
        assert gen_types[0] == "science"

    def test_generate_science_missing_topic(self, client):
        response = client.post("/api/generate/science", json={
            "audience": "general",
            "tone":     "divulgativo",
        })
        assert response.status_code == 422

    def test_generate_science_missing_audience(self, client):
        response = client.post("/api/generate/science", json={
            "topic": "artificial intelligence",
            "tone":  "divulgativo",
        })
        assert response.status_code == 422

    def test_generate_science_topic_not_found(self, client):
        response = client.post("/api/generate/science", json={
            "topic":    "xyzabc123notexist",
            "audience": "general",
            "tone":     "divulgativo",
            "language": "es",
        })
        # Puede devolver 404 si no encuentra papers o 200 con contenido genérico
        assert response.status_code in [200, 404, 500]