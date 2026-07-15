from app.models.metric import MetricType
from app.schemas.dashboard import DashboardResponse, MetricAnalytics, Trend


def test_metric_analytics_holds_trend() -> None:
    analytics = MetricAnalytics(avg_7d=7.5, avg_30d=7.0, trend=Trend(direction="up", pct_change=4.1))

    assert analytics.trend is not None
    assert analytics.trend.direction == "up"


def test_metric_analytics_allows_null_fields() -> None:
    analytics = MetricAnalytics(avg_7d=None, avg_30d=None, trend=None)

    assert analytics.avg_7d is None
    assert analytics.trend is None


def test_dashboard_response_defaults_ai_summary_to_none() -> None:
    response = DashboardResponse(
        latest={mt: None for mt in MetricType},
        metrics={mt: MetricAnalytics(avg_7d=None, avg_30d=None, trend=None) for mt in MetricType},
        health_score=None,
    )

    assert response.ai_summary is None
    assert response.health_score is None


def test_dashboard_response_serializes_metric_type_keys_as_strings() -> None:
    response = DashboardResponse(
        latest={mt: None for mt in MetricType},
        metrics={mt: MetricAnalytics(avg_7d=None, avg_30d=None, trend=None) for mt in MetricType},
        health_score=78,
    )

    dumped = response.model_dump(mode="json")

    assert "sleep" in dumped["metrics"]
    assert "heart_rate" in dumped["latest"]
