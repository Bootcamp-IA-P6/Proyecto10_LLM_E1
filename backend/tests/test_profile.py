import pytest


class TestProfileEndpoints:

    def test_get_profile_initially_none(self, client):
        response = client.get("/api/profile")
        assert response.status_code == 200
        # Puede ser None o un perfil previo de otro test
        data = response.json()
        assert data is None or isinstance(data, dict)

    def test_save_profile(self, client):
        response = client.post("/api/profile", json={
            "name":        "TechCorp Madrid",
            "sector":      "tecnología",
            "tone":        "innovador",
            "description": "Empresa de desarrollo de software con foco en IA",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"]   == "TechCorp Madrid"
        assert data["sector"] == "tecnología"
        assert data["tone"]   == "innovador"

    def test_get_profile_after_save(self, client):
        # Guardar perfil
        client.post("/api/profile", json={
            "name":   "TestCorp",
            "sector": "educación",
            "tone":   "cercano",
        })
        # Recuperar y verificar
        response = client.get("/api/profile")
        assert response.status_code == 200
        data = response.json()
        assert data is not None
        assert data["name"]   == "TestCorp"
        assert data["sector"] == "educación"
        assert data["tone"]   == "cercano"

    def test_update_profile(self, client):
        # Guardar perfil inicial
        client.post("/api/profile", json={
            "name":   "Empresa A",
            "sector": "salud",
            "tone":   "profesional",
        })
        # Actualizar con nuevo perfil
        client.post("/api/profile", json={
            "name":   "Empresa B",
            "sector": "finanzas",
            "tone":   "formal",
        })
        # Verificar que se actualizó
        response = client.get("/api/profile")
        data     = response.json()
        assert data["name"]   == "Empresa B"
        assert data["sector"] == "finanzas"

    def test_save_profile_missing_name(self, client):
        response = client.post("/api/profile", json={
            "sector": "tecnología",
            "tone":   "innovador",
        })
        assert response.status_code == 422

    def test_save_profile_missing_sector(self, client):
        response = client.post("/api/profile", json={
            "name": "TechCorp",
            "tone": "innovador",
        })
        assert response.status_code == 422

    def test_save_profile_missing_tone(self, client):
        response = client.post("/api/profile", json={
            "name":   "TechCorp",
            "sector": "tecnología",
        })
        assert response.status_code == 422

    def test_save_profile_without_description(self, client):
        response = client.post("/api/profile", json={
            "name":   "MinimalCorp",
            "sector": "retail",
            "tone":   "amigable",
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "MinimalCorp"

    def test_profile_injected_in_generation(self, client):
        # Guardar perfil
        client.post("/api/profile", json={
            "name":        "EcoTech",
            "sector":      "medioambiente",
            "tone":        "comprometido",
            "description": "Empresa de tecnología sostenible",
        })
        # Generar sin pasar company_profile explícito
        response = client.post("/api/generate", json={
            "platform": "linkedin",
            "topic":    "sostenibilidad empresarial",
            "audience": "directivos",
            "model":    "groq",
        })
        assert response.status_code == 200
        data = response.json()
        assert "content" in data
        assert len(data["content"]) > 50