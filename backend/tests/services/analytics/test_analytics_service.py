import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate
from app.services.analytics.analytics_service import AnalyticsService
from tests.auth_helpers import create_test_user_id


async def test_get_metric_analytics_computes_averages(db_session) -> None:
    repo = MetricRepository(db_session)
    service = AnalyticsService(repo)
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.SLEEP, value=6.0, recorded_at=now - timedelta(days=1)),
    )
    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.SLEEP, value=8.0, recorded_at=now - timedelta(days=3)),
    )

    result = await service.get_metric_analytics(user_id, MetricType.SLEEP, now=now)

    assert result.avg_7d == pytest.approx(7.0)


async def test_get_metric_analytics_trend_up(db_session) -> None:
    repo = MetricRepository(db_session)
    service = AnalyticsService(repo)
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.STEPS, value=10000, recorded_at=now - timedelta(days=2)),
    )
    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.STEPS, value=5000, recorded_at=now - timedelta(days=10)),
    )

    result = await service.get_metric_analytics(user_id, MetricType.STEPS, now=now)

    assert result.trend is not None
    assert result.trend.direction == "up"


async def test_get_metric_analytics_trend_stable_within_dead_band(db_session) -> None:
    repo = MetricRepository(db_session)
    service = AnalyticsService(repo)
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.WEIGHT, value=70.5, recorded_at=now - timedelta(days=2)),
    )
    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.WEIGHT, value=70.0, recorded_at=now - timedelta(days=10)),
    )

    result = await service.get_metric_analytics(user_id, MetricType.WEIGHT, now=now)

    assert result.trend is not None
    assert result.trend.direction == "stable"


async def test_get_metric_analytics_trend_none_without_prior_window_data(db_session) -> None:
    repo = MetricRepository(db_session)
    service = AnalyticsService(repo)
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.WATER, value=2.0, recorded_at=now - timedelta(days=1)),
    )

    result = await service.get_metric_analytics(user_id, MetricType.WATER, now=now)

    assert result.avg_7d == pytest.approx(2.0)
    assert result.trend is None


def test_compute_trend_direction_just_inside_stable_band() -> None:
    trend = AnalyticsService._compute_trend(avg_7d=101.9, avg_prior_7d=100.0)

    assert trend is not None
    assert trend.direction == "stable"


def test_compute_trend_direction_just_outside_stable_band() -> None:
    trend = AnalyticsService._compute_trend(avg_7d=102.1, avg_prior_7d=100.0)

    assert trend is not None
    assert trend.direction == "up"


async def test_get_metric_analytics_all_none_without_any_data(db_session) -> None:
    repo = MetricRepository(db_session)
    service = AnalyticsService(repo)

    result = await service.get_metric_analytics(
        uuid.uuid4(), MetricType.HEART_RATE, now=datetime.now(timezone.utc)
    )

    assert result.avg_7d is None
    assert result.avg_30d is None
    assert result.trend is None
