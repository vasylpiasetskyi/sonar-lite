from app.models.metric import MetricType
from app.schemas.dashboard import MetricAnalytics, Trend
from app.services.analytics.analytics_service import AnalyticsService


def _analytics(avg_7d: float | None = None, trend: Trend | None = None) -> MetricAnalytics:
    return MetricAnalytics(avg_7d=avg_7d, avg_30d=None, trend=trend)


def test_sleep_recommendation_fires_below_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.SLEEP: _analytics(avg_7d=5.0)}

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 1
    assert recommendations[0].metric_type == MetricType.SLEEP
    assert recommendations[0].message == "Improve sleep hygiene / schedule"


def test_sleep_recommendation_does_not_fire_at_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.SLEEP: _analytics(avg_7d=6.0)}

    assert service.evaluate_recommendations(metrics) == []


def test_heart_rate_recommendation_fires_above_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.HEART_RATE: _analytics(avg_7d=101.0)}

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 1
    assert recommendations[0].message == "Recommend consulting a healthcare professional"


def test_heart_rate_recommendation_does_not_fire_at_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.HEART_RATE: _analytics(avg_7d=100.0)}

    assert service.evaluate_recommendations(metrics) == []


def test_water_recommendation_fires_below_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.WATER: _analytics(avg_7d=1.0)}

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 1
    assert recommendations[0].message == "Increase hydration"


def test_water_recommendation_does_not_fire_at_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.WATER: _analytics(avg_7d=1.5)}

    assert service.evaluate_recommendations(metrics) == []


def test_steps_recommendation_fires_below_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.STEPS: _analytics(avg_7d=4000)}

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 1
    assert recommendations[0].message == "Increase daily activity"


def test_steps_recommendation_does_not_fire_at_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.STEPS: _analytics(avg_7d=5000)}

    assert service.evaluate_recommendations(metrics) == []


def test_weight_recommendation_fires_above_pct_change_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.WEIGHT: _analytics(trend=Trend(direction="up", pct_change=4.0))}

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 1
    assert recommendations[0].message == "Monitor nutrition, flag for attention"


def test_weight_recommendation_does_not_fire_within_threshold() -> None:
    service = AnalyticsService(repository=None)
    metrics = {MetricType.WEIGHT: _analytics(trend=Trend(direction="up", pct_change=3.0))}

    assert service.evaluate_recommendations(metrics) == []


def test_no_recommendations_when_no_data() -> None:
    service = AnalyticsService(repository=None)
    metrics = {mt: _analytics() for mt in MetricType}

    assert service.evaluate_recommendations(metrics) == []


def test_multiple_recommendations_fire_together() -> None:
    service = AnalyticsService(repository=None)
    metrics = {
        MetricType.SLEEP: _analytics(avg_7d=5.0),
        MetricType.STEPS: _analytics(avg_7d=3000),
    }

    recommendations = service.evaluate_recommendations(metrics)

    assert len(recommendations) == 2
    fired = {r.metric_type for r in recommendations}
    assert fired == {MetricType.SLEEP, MetricType.STEPS}
