from app.models.metric import MetricType
from app.schemas.recommendation import Recommendation


def test_recommendation_holds_metric_type_and_message() -> None:
    rec = Recommendation(metric_type=MetricType.SLEEP, message="Improve sleep hygiene / schedule")

    assert rec.metric_type == MetricType.SLEEP
    assert rec.message == "Improve sleep hygiene / schedule"
