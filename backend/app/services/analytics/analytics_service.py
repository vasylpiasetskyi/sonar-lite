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

    def compute_health_score(self, metrics: dict[MetricType, MetricAnalytics]) -> int | None:
        components: list[tuple[float, float]] = []

        sleep = metrics.get(MetricType.SLEEP)
        if sleep is not None and sleep.avg_7d is not None:
            components.append((0.30, self._sleep_score(sleep.avg_7d)))

        heart_rate = metrics.get(MetricType.HEART_RATE)
        if heart_rate is not None and heart_rate.avg_7d is not None:
            components.append((0.20, self._heart_rate_score(heart_rate.avg_7d)))

        water = metrics.get(MetricType.WATER)
        if water is not None and water.avg_7d is not None:
            components.append((0.10, self._water_score(water.avg_7d)))

        steps = metrics.get(MetricType.STEPS)
        if steps is not None and steps.avg_7d is not None:
            components.append((0.25, self._steps_score(steps.avg_7d)))

        weight = metrics.get(MetricType.WEIGHT)
        if weight is not None and weight.trend is not None:
            components.append((0.15, self._weight_stability_score(weight.trend.pct_change)))

        if not components:
            return None

        weighted_sum = sum(weight * score for weight, score in components)
        total_weight = sum(weight for weight, _ in components)
        return round(weighted_sum / total_weight)

    @staticmethod
    def _sleep_score(avg: float) -> float:
        if avg < 6:
            return 40
        if avg <= 9:
            return 100
        return 80

    @staticmethod
    def _heart_rate_score(avg: float) -> float:
        if avg < 45:
            return 0
        if avg <= 59:
            return 60
        if avg <= 100:
            return 100
        return 50

    @staticmethod
    def _water_score(avg: float) -> float:
        if avg < 1.5:
            return 50
        if avg <= 3:
            return 100
        return 80

    @staticmethod
    def _steps_score(avg: float) -> float:
        if avg < 5000:
            return 50
        if avg <= 10000:
            return 90
        return 100

    @staticmethod
    def _weight_stability_score(pct_change: float) -> float:
        return 100 if abs(pct_change) <= 3 else 60
