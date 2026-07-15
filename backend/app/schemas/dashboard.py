from datetime import datetime

from pydantic import BaseModel

from app.models.metric import MetricType


class Trend(BaseModel):
    direction: str
    pct_change: float


class MetricAnalytics(BaseModel):
    avg_7d: float | None
    avg_30d: float | None
    trend: Trend | None


class LatestReading(BaseModel):
    value: float
    recorded_at: datetime


class DashboardResponse(BaseModel):
    latest: dict[MetricType, LatestReading | None]
    metrics: dict[MetricType, MetricAnalytics]
    health_score: int | None
    ai_summary: None = None
