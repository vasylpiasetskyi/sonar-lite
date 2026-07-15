from app.models.metric import MetricType
from app.schemas.ai_summary import AISummary, AISummaryContent
from app.schemas.dashboard import MetricAnalytics
from app.schemas.recommendation import Recommendation
from app.services.ai.prompts import build_summary_prompt
from app.services.ai.providers import AIProvider

DISCLAIMER_TEXT = "Recommendations are informational only, not medical advice."


class AISummaryGenerationError(Exception):
    pass


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    async def generate_summary(
        self,
        metrics: dict[MetricType, MetricAnalytics],
        recommendations: list[Recommendation],
    ) -> AISummary:
        prompt = build_summary_prompt(metrics, recommendations)

        for _ in range(2):
            raw_response = await self._provider.complete(prompt)
            try:
                content = AISummaryContent.model_validate_json(raw_response)
            except ValueError:
                continue
            return AISummary(**content.model_dump(), disclaimer=DISCLAIMER_TEXT)

        raise AISummaryGenerationError(
            "AI summary generation failed after retry: invalid or malformed response"
        )
