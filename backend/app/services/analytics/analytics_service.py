import uuid
from datetime import datetime, timedelta, timezone

from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.dashboard import MetricAnalytics, Trend

TREND_STABLE_BAND_PCT = 2.0


class AnalyticsService:
    def __init__(self, repository: MetricRepository) -> None:
        self._repository = repository

    async def get_metric_analytics(
        self, user_id: uuid.UUID, metric_type: MetricType, now: datetime | None = None
    ) -> MetricAnalytics:
        now = now or datetime.now(timezone.utc)

        avg_7d = await self._repository.average(
            user_id, metric_type, now - timedelta(days=7), now
        )
        avg_30d = await self._repository.average(
            user_id, metric_type, now - timedelta(days=30), now
        )
        avg_prior_7d = await self._repository.average(
            user_id, metric_type, now - timedelta(days=14), now - timedelta(days=7)
        )

        return MetricAnalytics(
            avg_7d=avg_7d,
            avg_30d=avg_30d,
            trend=self._compute_trend(avg_7d, avg_prior_7d),
        )

    @staticmethod
    def _compute_trend(avg_7d: float | None, avg_prior_7d: float | None) -> Trend | None:
        if avg_7d is None or avg_prior_7d is None:
            return None

        pct_change = (avg_7d - avg_prior_7d) / avg_prior_7d * 100

        if abs(pct_change) < TREND_STABLE_BAND_PCT:
            direction = "stable"
        elif pct_change > 0:
            direction = "up"
        else:
            direction = "down"

        return Trend(direction=direction, pct_change=round(pct_change, 1))
