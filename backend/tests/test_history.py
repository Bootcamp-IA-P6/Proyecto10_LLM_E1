import pytest


class TestHistoryEndpoints:

    def test_get_history_empty_or_list(self, client):
        response = client.get("/api/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_history_saved_after_generation(self, client):
        # Generar contenido
        client.post("/api/generate", json={
            "platform": "blog",
            "topic":    "test history save",
            "audience": "testers",
            "model":    "groq",
        })
        # Verificar que aparece en historial
        response = client.get("/api/history")
        assert response.status_code == 200
        topics = [h["topic"] for h in response.json()]
        assert "test history save" in topics

    def test_history_record_has_required_fields(self, client):
        # Generar contenido
        client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "test fields check",
            "audience": "testers",
            "model":    "groq",
        })
        response = client.get("/api/history")
        data     = response.json()
        assert len(data) > 0

        record = data[0]
        assert "id"         in record
        assert "platform"   in record
        assert "topic"      in record
        assert "audience"   in record
        assert "content"    in record
        assert "model_used" in record
        assert "gen_type"   in record
        assert "created_at" in record

    def test_history_has_quality_fields(self, client):
        client.post("/api/generate", json={
            "platform": "linkedin",
            "topic":    "test quality fields",
            "audience": "testers",
            "model":    "groq",
        })
        response = client.get("/api/history")
        data     = response.json()
        assert len(data) > 0

        record = data[0]
        assert "quality_score"    in record
        assert "quality_feedback" in record

    def test_history_limit_param(self, client):
        # Generar varios contenidos
        for i in range(3):
            client.post("/api/generate", json={
                "platform": "twitter",
                "topic":    f"test limit {i}",
                "audience": "testers",
                "model":    "groq",
            })
        # Pedir solo 2
        response = client.get("/api/history?limit=2")
        assert response.status_code == 200
        assert len(response.json()) <= 2

    def test_history_skip_param(self, client):
        response_all  = client.get("/api/history?limit=10&skip=0")
        response_skip = client.get("/api/history?limit=10&skip=1")
        assert response_all.status_code  == 200
        assert response_skip.status_code == 200

        all_data  = response_all.json()
        skip_data = response_skip.json()

        if len(all_data) > 1:
            assert all_data[0]["id"] != skip_data[0]["id"]

    def test_delete_generation(self, client):
        # Generar contenido
        client.post("/api/generate", json={
            "platform": "blog",
            "topic":    "test delete me",
            "audience": "testers",
            "model":    "groq",
        })
        # Obtener el ID del registro
        history    = client.get("/api/history").json()
        record_ids = [h["id"] for h in history if h["topic"] == "test delete me"]
        assert len(record_ids) > 0

        record_id = record_ids[0]

        # Borrar
        response = client.delete(f"/api/history/{record_id}")
        assert response.status_code == 200
        assert response.json()["deleted"] is True

        # Verificar que ya no existe
        history_after = client.get("/api/history").json()
        ids_after     = [h["id"] for h in history_after]
        assert record_id not in ids_after

    def test_delete_nonexistent_generation(self, client):
        response = client.delete("/api/history/99999")
        assert response.status_code == 404

    def test_history_ordered_by_most_recent(self, client):
        # Generar dos contenidos en orden
        client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "test orden primero",
            "audience": "testers",
            "model":    "groq",
        })
        client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "test orden segundo",
            "audience": "testers",
            "model":    "groq",
        })
        history = client.get("/api/history").json()
        assert len(history) >= 2
        # El más reciente debe ser el primero
        assert history[0]["topic"] == "test orden segundo"

    def test_history_gen_type_general(self, client):
        client.post("/api/generate", json={
            "platform": "twitter",
            "topic":    "test gen type social",
            "audience": "testers",
            "model":    "groq",
        })
        history  = client.get("/api/history").json()
        gen_type = history[0]["gen_type"]
        assert gen_type in ["blog", "social", "science", "finance", "general"]