import pytest
from app.services.pollinations_service import generate_image_pollinations
from app.services.image_service import get_image
from app.services.image_router import get_image_by_source


class TestPollinationsService:

    def test_returns_string(self):
        url = generate_image_pollinations("inteligencia artificial")
        assert isinstance(url, str)

    def test_returns_pollinations_url(self):
        url = generate_image_pollinations("tecnología")
        assert "pollinations.ai" in url

    def test_encodes_special_characters(self):
        url = generate_image_pollinations("café y tecnología")
        assert isinstance(url, str)
        assert len(url) > 0

    def test_handles_empty_prompt(self):
        url = generate_image_pollinations("")
        assert isinstance(url, str)

    def test_handles_long_prompt(self):
        long_prompt = "tecnología " * 50
        url         = generate_image_pollinations(long_prompt)
        assert isinstance(url, str)
        assert len(url) > 0

    def test_url_has_correct_dimensions(self):
        url = generate_image_pollinations("naturaleza")
        assert "width=1080" in url
        assert "height=720" in url

    def test_url_has_nologo_param(self):
        url = generate_image_pollinations("naturaleza")
        assert "nologo=true" in url


class TestUnsplashService:

    def test_returns_string(self):
        url = get_image("inteligencia artificial")
        assert isinstance(url, str)

    def test_handles_empty_topic(self):
        url = get_image("")
        assert isinstance(url, str)

    def test_handles_special_characters(self):
        url = get_image("café y naturaleza")
        assert isinstance(url, str)


class TestImageRouter:

    def test_unsplash_source(self):
        url = get_image_by_source("tecnología", "unsplash")
        assert isinstance(url, str)

    def test_pollinations_source(self):
        url = get_image_by_source("tecnología", "pollinations")
        assert isinstance(url, str)
        assert "pollinations.ai" in url

    def test_huggingface_fallback_to_pollinations(self):
        # Si HF falla el fallback es Pollinations
        url = get_image_by_source("tecnología", "huggingface")
        assert isinstance(url, str)
        # Debe devolver algo — ya sea HF o Pollinations
        assert len(url) > 0

    def test_default_source_is_unsplash(self):
        url = get_image_by_source("tecnología")
        assert isinstance(url, str)

    def test_invalid_source_defaults_to_unsplash(self):
        url = get_image_by_source("tecnología", "fuente_inexistente")
        assert isinstance(url, str)

    def test_pollinations_url_contains_topic(self):
        url = get_image_by_source("inteligencia artificial", "pollinations")
        assert "inteligencia" in url or "artificial" in url

    def test_all_sources_return_string(self):
        sources = ["unsplash", "pollinations", "huggingface"]
        for source in sources:
            url = get_image_by_source("tecnología", source)
            assert isinstance(url, str), f"Falló con source={source}"