import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.metric import MetricType
from app.schemas.metric import MetricCreate, MetricRead


def test_metric_create_accepts_valid_data() -> None:
    metric = MetricCreate(
        metric_type=MetricType.SLEEP, value=7.5, recorded_at=datetime.now(timezone.utc)
    )
    assert metric.value == 7.5


def test_metric_create_rejects_non_positive_value() -> None:
    with pytest.raises(ValidationError):
        MetricCreate(
            metric_type=MetricType.SLEEP, value=0, recorded_at=datetime.now(timezone.utc)
        )


def test_metric_create_rejects_invalid_metric_type() -> None:
    with pytest.raises(ValidationError):
        MetricCreate(metric_type="invalid", value=5, recorded_at=datetime.now(timezone.utc))


def test_metric_read_serializes_from_orm_style_object() -> None:
    class FakeOrmMetric:
        id = uuid.uuid4()
        user_id = uuid.uuid4()
        metric_type = MetricType.WEIGHT
        value = 70.5
        recorded_at = datetime.now(timezone.utc)
        created_at = datetime.now(timezone.utc)
        updated_at = datetime.now(timezone.utc)

    read = MetricRead.model_validate(FakeOrmMetric())
    assert read.value == 70.5
