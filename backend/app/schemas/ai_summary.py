from pydantic import BaseModel

from app.schemas.recommendation import Recommendation


class AISummaryContent(BaseModel):
    summary: str
    positive_observations: list[str]
    risks: list[str]
    recommendations: list[str]
    next_week_focus: str


class AISummary(AISummaryContent):
    disclaimer: str


class AISummaryResponse(BaseModel):
    rule_based_recommendations: list[Recommendation]
    ai_summary: AISummary | None
    ai_summary_error: str | None
