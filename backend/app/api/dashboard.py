from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.repositories.metric_repository import MetricRepository
from app.schemas.dashboard import DashboardResponse
from app.services.analytics.analytics_service import AnalyticsService
from app.services.dashboard.dashboard_service import DashboardService

router = APIRouter(tags=["dashboard"])


def get_dashboard_service(db: AsyncSession = Depends(get_db)) -> DashboardService:
    repository = MetricRepository(db)
    return DashboardService(repository, AnalyticsService(repository))


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    service: DashboardService = Depends(get_dashboard_service),
) -> DashboardResponse:
    return await service.get_dashboard()
