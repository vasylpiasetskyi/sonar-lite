import pytest

from app.core.config import Settings
from app.services.ai.factory import get_ai_provider
from app.services.ai.providers import MockAIProvider, OpenAIProvider


def test_get_ai_provider_returns_mock_by_default() -> None:
    settings = Settings(ai_provider="mock")

    provider = get_ai_provider(settings)

    assert isinstance(provider, MockAIProvider)


def test_get_ai_provider_returns_openai_when_configured_with_key() -> None:
    settings = Settings(ai_provider="openai", openai_api_key="test-key")

    provider = get_ai_provider(settings)

    assert isinstance(provider, OpenAIProvider)


def test_get_ai_provider_raises_when_openai_selected_without_key() -> None:
    settings = Settings(ai_provider="openai", openai_api_key=None)

    with pytest.raises(RuntimeError):
        get_ai_provider(settings)
