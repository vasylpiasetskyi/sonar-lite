import uuid
from datetime import datetime, timedelta, timezone

from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate
from app.services.analytics.analytics_service import AnalyticsService
from app.services.dashboard.dashboard_service import DashboardService
from tests.auth_helpers import create_test_user_id


async def test_get_dashboard_returns_latest_and_metrics_for_given_user(db_session) -> None:
    repo = MetricRepository(db_session)
    service = DashboardService(repo, AnalyticsService(repo))
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(metric_type=MetricType.SLEEP, value=7.0, recorded_at=now - timedelta(hours=2)),
    )

    result = await service.get_dashboard(user_id, now=now)

    assert result.latest[MetricType.SLEEP] is not None
    assert result.latest[MetricType.SLEEP].value == 7.0
    assert result.latest[MetricType.WEIGHT] is None
    assert result.metrics[MetricType.SLEEP].avg_7d == 7.0
    assert result.ai_summary is None


async def test_get_dashboard_health_score_reflects_recorded_metrics(db_session) -> None:
    repo = MetricRepository(db_session)
    service = DashboardService(repo, AnalyticsService(repo))
    user_id = await create_test_user_id(db_session)
    now = datetime.now(timezone.utc)

    await repo.create(
        user_id,
        MetricCreate(
            metric_type=MetricType.HEART_RATE, value=70.0, recorded_at=now - timedelta(hours=1)
        ),
    )

    result = await service.get_dashboard(user_id, now=now)

    assert result.health_score == 100


async def test_get_dashboard_health_score_none_without_any_metrics(db_session) -> None:
    repo = MetricRepository(db_session)
    service = DashboardService(repo, AnalyticsService(repo))
    user_id = uuid.uuid4()

    result = await service.get_dashboard(user_id, now=datetime.now(timezone.utc))

    assert result.health_score is None
