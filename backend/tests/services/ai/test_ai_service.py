import pytest

from app.models.metric import MetricType
from app.schemas.dashboard import MetricAnalytics
from app.services.ai.ai_service import AIService, AISummaryGenerationError
from app.services.ai.providers import MockAIProvider

VALID_RESPONSE = (
    '{"summary": "Test summary.", "positive_observations": ["Good sleep."], '
    '"risks": ["Low water."], "recommendations": ["Drink more water."], '
    '"next_week_focus": "Hydration."}'
)


async def test_generate_summary_succeeds_on_first_valid_response() -> None:
    provider = MockAIProvider(responses=[VALID_RESPONSE])
    service = AIService(provider)
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=7.0, avg_30d=7.0, trend=None)}

    summary = await service.generate_summary(metrics, [])

    assert summary.summary == "Test summary."
    assert summary.disclaimer == "Recommendations are informational only, not medical advice."


async def test_generate_summary_retries_once_then_succeeds() -> None:
    provider = MockAIProvider(responses=["not valid json", VALID_RESPONSE])
    service = AIService(provider)
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=7.0, avg_30d=7.0, trend=None)}

    summary = await service.generate_summary(metrics, [])

    assert summary.summary == "Test summary."


async def test_generate_summary_raises_after_retry_also_fails() -> None:
    provider = MockAIProvider(responses=["not valid json", "still not valid json"])
    service = AIService(provider)
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=7.0, avg_30d=7.0, trend=None)}

    with pytest.raises(AISummaryGenerationError):
        await service.generate_summary(metrics, [])


async def test_generate_summary_ignores_llm_supplied_disclaimer() -> None:
    response_with_bogus_disclaimer = (
        '{"summary": "Test summary.", "positive_observations": [], '
        '"risks": [], "recommendations": [], "next_week_focus": "Focus.", '
        '"disclaimer": "Trust me, this is definitely medical advice."}'
    )
    provider = MockAIProvider(responses=[response_with_bogus_disclaimer])
    service = AIService(provider)
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=7.0, avg_30d=7.0, trend=None)}

    summary = await service.generate_summary(metrics, [])

    assert summary.disclaimer == "Recommendations are informational only, not medical advice."


class _RaisingProvider:
    async def complete(self, prompt: str) -> str:
        raise ConnectionError("upstream AI provider unreachable")


async def test_generate_summary_raises_ai_error_when_provider_itself_fails() -> None:
    service = AIService(_RaisingProvider())
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=7.0, avg_30d=7.0, trend=None)}

    with pytest.raises(AISummaryGenerationError):
        await service.generate_summary(metrics, [])
