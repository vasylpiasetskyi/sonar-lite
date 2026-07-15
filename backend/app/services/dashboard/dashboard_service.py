from datetime import datetime, timezone

from app.core.constants import DEMO_USER_ID
from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.dashboard import DashboardResponse, LatestReading, MetricAnalytics
from app.services.analytics.analytics_service import AnalyticsService


class DashboardService:
    def __init__(self, repository: MetricRepository, analytics: AnalyticsService) -> None:
        self._repository = repository
        self._analytics = analytics

    async def get_dashboard(self, now: datetime | None = None) -> DashboardResponse:
        now = now or datetime.now(timezone.utc)

        latest: dict[MetricType, LatestReading | None] = {}
        metrics: dict[MetricType, MetricAnalytics] = {}

        for metric_type in MetricType:
            latest_metric = await self._repository.latest(DEMO_USER_ID, metric_type)
            latest[metric_type] = (
                LatestReading(value=latest_metric.value, recorded_at=latest_metric.recorded_at)
                if latest_metric is not None
                else None
            )
            metrics[metric_type] = await self._analytics.get_metric_analytics(
                DEMO_USER_ID, metric_type, now=now
            )

        health_score = self._analytics.compute_health_score(metrics)

        return DashboardResponse(
            latest=latest,
            metrics=metrics,
            health_score=health_score,
            ai_summary=None,
        )
