import pytest


class TestNewsEndpoints:

    def test_get_financial_news(self, client):
        response = client.get("/api/news/financial")
        assert response.status_code == 200
        data = response.json()
        assert "topic" in data
        assert "count" in data
        assert "news"  in data
        assert isinstance(data["news"], list)

    def test_get_financial_news_has_required_fields(self, client):
        response = client.get("/api/news/financial")
        assert response.status_code == 200
        data = response.json()

        if len(data["news"]) > 0:
            headline = data["news"][0]
            assert "title"       in headline
            assert "description" in headline
            assert "url"         in headline

    def test_get_financial_news_with_topic(self, client):
        response = client.get("/api/news/financial?topic=bitcoin")
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "bitcoin"
        assert isinstance(data["news"], list)

    def test_get_financial_news_default_topic(self, client):
        response = client.get("/api/news/financial")
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "bolsa mercados finanzas"

    def test_generate_news_content(self, client):
        response = client.post("/api/generate/news", json={
            "topic":    "bolsa española",
            "platform": "linkedin",
            "audience": "inversores",
            "tone":     "profesional",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content"    in data
        assert "model_used" in data
        assert len(data["content"]) > 50

    def test_generate_news_returns_image_url(self, client):
        response = client.post("/api/generate/news", json={
            "topic":    "mercados financieros",
            "platform": "twitter",
            "audience": "inversores",
            "tone":     "informativo",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "image_url" in data

    def test_generate_news_twitter(self, client):
        response = client.post("/api/generate/news", json={
            "topic":    "criptomonedas",
            "platform": "twitter",
            "audience": "inversores jóvenes",
            "tone":     "informal",
            "language": "es",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert data["platform"] == "twitter"

    def test_generate_news_in_english(self, client):
        response = client.post("/api/generate/news", json={
            "topic":    "stock market",
            "platform": "linkedin",
            "audience": "investors",
            "tone":     "professional",
            "language": "en",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 50

    def test_generate_news_missing_topic(self, client):
        response = client.post("/api/generate/news", json={
            "platform": "linkedin",
            "audience": "inversores",
        })
        assert response.status_code == 422

    def test_generate_news_missing_platform(self, client):
        response = client.post("/api/generate/news", json={
            "topic":    "bolsa",
            "audience": "inversores",
        })
        assert response.status_code == 422

    def test_generate_news_saves_to_history(self, client):
        client.post("/api/generate/news", json={
            "topic":    "test news history",
            "platform": "linkedin",
            "audience": "testers",
            "tone":     "profesional",
            "language": "es",
        })
        history = client.get("/api/history").json()
        topics  = [h["topic"] for h in history]
        assert "test news history" in topics

    def test_generate_news_gen_type(self, client):
        client.post("/api/generate/news", json={
            "topic":    "test gen type news",
            "platform": "twitter",
            "audience": "testers",
            "tone":     "informativo",
            "language": "es",
        })
        history  = client.get("/api/history").json()
        gen_types = [h["gen_type"] for h in history
                     if h["topic"] == "test gen type news"]
        assert len(gen_types) > 0
        assert gen_types[0] == "news"