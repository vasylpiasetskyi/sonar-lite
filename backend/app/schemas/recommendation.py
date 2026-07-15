from pydantic import BaseModel

from app.models.metric import MetricType


class Recommendation(BaseModel):
    metric_type: MetricType
    message: str
