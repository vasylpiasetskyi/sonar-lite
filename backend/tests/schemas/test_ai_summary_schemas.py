from app.models.metric import MetricType
from app.schemas.ai_summary import AISummary, AISummaryContent, AISummaryResponse
from app.schemas.recommendation import Recommendation


def test_ai_summary_content_requires_all_fields() -> None:
    content = AISummaryContent(
        summary="...",
        positive_observations=["..."],
        risks=["..."],
        recommendations=["..."],
        next_week_focus="...",
    )

    assert content.summary == "..."


def test_ai_summary_adds_disclaimer_on_top_of_content() -> None:
    summary = AISummary(
        summary="...",
        positive_observations=[],
        risks=[],
        recommendations=[],
        next_week_focus="...",
        disclaimer="Recommendations are informational only, not medical advice.",
    )

    assert summary.disclaimer == "Recommendations are informational only, not medical advice."


def test_ai_summary_response_allows_null_summary_and_error() -> None:
    response = AISummaryResponse(
        rule_based_recommendations=[
            Recommendation(
                metric_type=MetricType.SLEEP, message="Improve sleep hygiene / schedule"
            )
        ],
        ai_summary=None,
        ai_summary_error="AI summary generation failed after retry: invalid JSON",
    )

    assert response.ai_summary is None
    assert response.ai_summary_error is not None
