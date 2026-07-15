from app.models.metric import MetricType
from app.schemas.dashboard import MetricAnalytics, Trend
from app.services.analytics.analytics_service import AnalyticsService


def _analytics(avg_7d: float | None = None, trend: Trend | None = None) -> MetricAnalytics:
    return MetricAnalytics(avg_7d=avg_7d, avg_30d=None, trend=trend)


def test_compute_health_score_all_components_present() -> None:
    service = AnalyticsService(repository=None)

    metrics = {
        MetricType.SLEEP: _analytics(avg_7d=7.0),
        MetricType.HEART_RATE: _analytics(avg_7d=70.0),
        MetricType.WATER: _analytics(avg_7d=2.0),
        MetricType.STEPS: _analytics(avg_7d=8000),
        MetricType.WEIGHT: _analytics(trend=Trend(direction="stable", pct_change=1.0)),
    }

    score = service.compute_health_score(metrics)

    assert score == 98


def test_compute_health_score_renormalizes_when_component_missing() -> None:
    service = AnalyticsService(repository=None)

    metrics = {
        MetricType.SLEEP: _analytics(),
        MetricType.HEART_RATE: _analytics(avg_7d=70.0),
        MetricType.WATER: _analytics(),
        MetricType.STEPS: _analytics(),
        MetricType.WEIGHT: _analytics(),
    }

    score = service.compute_health_score(metrics)

    assert score == 100


def test_compute_health_score_none_when_no_components_present() -> None:
    service = AnalyticsService(repository=None)

    metrics = {mt: _analytics() for mt in MetricType}

    score = service.compute_health_score(metrics)

    assert score is None


def test_sleep_score_boundaries() -> None:
    service = AnalyticsService(repository=None)

    assert service._sleep_score(5.9) == 40
    assert service._sleep_score(6.0) == 100
    assert service._sleep_score(9.0) == 100
    assert service._sleep_score(9.1) == 80


def test_heart_rate_score_boundaries() -> None:
    service = AnalyticsService(repository=None)

    assert service._heart_rate_score(44.9) == 0
    assert service._heart_rate_score(45.0) == 60
    assert service._heart_rate_score(59.0) == 60
    assert service._heart_rate_score(60.0) == 100
    assert service._heart_rate_score(100.0) == 100
    assert service._heart_rate_score(100.1) == 50


def test_water_score_boundaries() -> None:
    service = AnalyticsService(repository=None)

    assert service._water_score(1.4) == 50
    assert service._water_score(1.5) == 100
    assert service._water_score(3.0) == 100
    assert service._water_score(3.1) == 80


def test_steps_score_boundaries() -> None:
    service = AnalyticsService(repository=None)

    assert service._steps_score(4999) == 50
    assert service._steps_score(5000) == 90
    assert service._steps_score(10000) == 90
    assert service._steps_score(10001) == 100


def test_weight_stability_score_boundaries() -> None:
    service = AnalyticsService(repository=None)

    assert service._weight_stability_score(3.0) == 100
    assert service._weight_stability_score(-3.0) == 100
    assert service._weight_stability_score(3.1) == 60
    assert service._weight_stability_score(-3.1) == 60
