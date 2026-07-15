from app.core.config import Settings
from app.services.ai.providers import AIProvider, MockAIProvider, OpenAIProvider


def get_ai_provider(settings: Settings) -> AIProvider:
    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise RuntimeError(
                "ai_provider is set to 'openai' but openai_api_key is not configured"
            )
        return OpenAIProvider(api_key=settings.openai_api_key)
    return MockAIProvider()
