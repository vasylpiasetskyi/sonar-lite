from app.models.metric import MetricType
from app.schemas.dashboard import MetricAnalytics, Trend
from app.schemas.recommendation import Recommendation
from app.services.ai.prompts import build_summary_prompt


def test_build_summary_prompt_includes_metric_averages() -> None:
    metrics = {
        MetricType.SLEEP: MetricAnalytics(
            avg_7d=5.5, avg_30d=6.0, trend=Trend(direction="down", pct_change=-5.0)
        )
    }

    prompt = build_summary_prompt(metrics, [])

    assert "sleep" in prompt
    assert "5.5" in prompt
    assert "down" in prompt


def test_build_summary_prompt_includes_recommendations() -> None:
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=None, avg_30d=None, trend=None)}
    recommendations = [
        Recommendation(metric_type=MetricType.SLEEP, message="Improve sleep hygiene / schedule")
    ]

    prompt = build_summary_prompt(metrics, recommendations)

    assert "Improve sleep hygiene / schedule" in prompt


def test_build_summary_prompt_handles_no_recommendations() -> None:
    metrics = {MetricType.SLEEP: MetricAnalytics(avg_7d=None, avg_30d=None, trend=None)}

    prompt = build_summary_prompt(metrics, [])

    assert "None." in prompt


def test_build_summary_prompt_requests_json_only() -> None:
    prompt = build_summary_prompt({}, [])

    assert "JSON" in prompt
