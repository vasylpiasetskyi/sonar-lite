from datetime import datetime, timezone

from app.core.constants import DEMO_USER_ID
from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate, MetricUpdate
from app.services.metrics.metric_service import MetricService


async def test_create_uses_demo_user_id(db_session) -> None:
    service = MetricService(MetricRepository(db_session))

    metric = await service.create(
        MetricCreate(
            metric_type=MetricType.SLEEP, value=8.0, recorded_at=datetime.now(timezone.utc)
        )
    )

    assert metric.user_id == DEMO_USER_ID


async def test_get_returns_metric_created_via_service(db_session) -> None:
    service = MetricService(MetricRepository(db_session))

    created = await service.create(
        MetricCreate(
            metric_type=MetricType.WATER, value=2.0, recorded_at=datetime.now(timezone.utc)
        )
    )
    fetched = await service.get(created.id)

    assert fetched is not None
    assert fetched.id == created.id


async def test_update_and_delete_roundtrip(db_session) -> None:
    service = MetricService(MetricRepository(db_session))

    created = await service.create(
        MetricCreate(
            metric_type=MetricType.WEIGHT, value=70, recorded_at=datetime.now(timezone.utc)
        )
    )
    updated = await service.update(created.id, MetricUpdate(value=71))
    assert updated is not None
    assert updated.value == 71

    deleted = await service.delete(created.id)
    assert deleted is True

    gone = await service.get(created.id)
    assert gone is None
