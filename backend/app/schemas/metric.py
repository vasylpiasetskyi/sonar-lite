import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.metric import MetricType


class MetricCreate(BaseModel):
    metric_type: MetricType
    value: float = Field(gt=0)
    recorded_at: datetime


class MetricUpdate(BaseModel):
    value: float | None = Field(default=None, gt=0)
    recorded_at: datetime | None = None


class MetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    metric_type: MetricType
    value: float
    recorded_at: datetime
    created_at: datetime
    updated_at: datetime


class MetricList(BaseModel):
    items: list[MetricRead]
    total: int
