import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.core.security_deps import get_current_user_id
from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.ai_summary import AISummaryResponse
from app.schemas.dashboard import MetricAnalytics
from app.services.ai.ai_service import AIService, AISummaryGenerationError
from app.services.ai.factory import get_ai_provider
from app.services.analytics.analytics_service import AnalyticsService

router = APIRouter(tags=["ai"])


def get_analytics_service(db: AsyncSession = Depends(get_db)) -> AnalyticsService:
    return AnalyticsService(MetricRepository(db))


def get_ai_service() -> AIService:
    return AIService(get_ai_provider(settings))


@router.post("/ai/summary", response_model=AISummaryResponse)
async def generate_ai_summary(
    user_id: uuid.UUID = Depends(get_current_user_id),
    analytics: AnalyticsService = Depends(get_analytics_service),
    ai_service: AIService = Depends(get_ai_service),
) -> AISummaryResponse:
    metrics: dict[MetricType, MetricAnalytics] = {}
    for metric_type in MetricType:
        metrics[metric_type] = await analytics.get_metric_analytics(user_id, metric_type)

    recommendations = analytics.evaluate_recommendations(metrics)

    try:
        ai_summary = await ai_service.generate_summary(metrics, recommendations)
        ai_summary_error = None
    except AISummaryGenerationError as exc:
        ai_summary = None
        ai_summary_error = str(exc)

    return AISummaryResponse(
        rule_based_recommendations=recommendations,
        ai_summary=ai_summary,
        ai_summary_error=ai_summary_error,
    )
