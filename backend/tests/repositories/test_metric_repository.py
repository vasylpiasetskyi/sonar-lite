import uuid
from datetime import datetime, timedelta, timezone

from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate, MetricUpdate


async def test_create_persists_metric(db_session) -> None:
    repo = MetricRepository(db_session)
    user_id = uuid.uuid4()

    metric = await repo.create(
        user_id,
        MetricCreate(
            metric_type=MetricType.WEIGHT, value=70.5, recorded_at=datetime.now(timezone.utc)
        ),
    )

    assert metric.id is not None
    assert metric.value == 70.5


async def test_get_returns_none_for_missing_metric(db_session) -> None:
    repo = MetricRepository(db_session)
    result = await repo.get(uuid.uuid4(), uuid.uuid4())
    assert result is None


async def test_get_returns_none_for_wrong_user(db_session) -> None:
    repo = MetricRepository(db_session)
    user_id = uuid.uuid4()
    other_user_id = uuid.uuid4()

    metric = await repo.create(
        user_id,
        MetricCreate(
            metric_type=MetricType.WATER, value=2.0, recorded_at=datetime.now(timezone.utc)
        ),
    )

    result = await repo.get(other_user_id, metric.id)
    assert result is None


async def test_list_filters_by_metric_type_and_paginates(db_session) -> None:
    repo = MetricRepository(db_session)
    user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    for i in range(3):
        await repo.create(
            user_id,
            MetricCreate(
                metric_type=MetricType.STEPS,
                value=1000 + i,
                recorded_at=now - timedelta(days=i),
            ),
        )
    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.SLEEP, value=7.0, recorded_at=now),
    )

    items, total = await repo.list(user_id, metric_type=MetricType.STEPS, limit=2, offset=0)

    assert total == 3
    assert len(items) == 2
    assert all(item.metric_type == MetricType.STEPS for item in items)


async def test_update_changes_value(db_session) -> None:
    repo = MetricRepository(db_session)
    user_id = uuid.uuid4()

    metric = await repo.create(
        user_id,
        MetricCreate(
            metric_type=MetricType.HEART_RATE, value=65, recorded_at=datetime.now(timezone.utc)
        ),
    )

    updated = await repo.update(user_id, metric.id, MetricUpdate(value=70))

    assert updated is not None
    assert updated.value == 70


async def test_update_returns_none_for_missing_metric(db_session) -> None:
    repo = MetricRepository(db_session)
    result = await repo.update(uuid.uuid4(), uuid.uuid4(), MetricUpdate(value=10))
    assert result is None


async def test_delete_removes_metric(db_session) -> None:
    repo = MetricRepository(db_session)
    user_id = uuid.uuid4()

    metric = await repo.create(
        user_id,
        MetricCreate(
            metric_type=MetricType.WATER, value=1.5, recorded_at=datetime.now(timezone.utc)
        ),
    )

    deleted = await repo.delete(user_id, metric.id)
    still_there = await repo.get(user_id, metric.id)

    assert deleted is True
    assert still_there is None


async def test_delete_returns_false_for_missing_metric(db_session) -> None:
    repo = MetricRepository(db_session)
    result = await repo.delete(uuid.uuid4(), uuid.uuid4())
    assert result is False
