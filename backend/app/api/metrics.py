import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.security_deps import get_current_user_id
from app.models.metric import MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate, MetricList, MetricRead, MetricUpdate
from app.services.metrics.metric_service import MetricService

router = APIRouter(prefix="/metrics", tags=["metrics"])


def get_metric_service(db: AsyncSession = Depends(get_db)) -> MetricService:
    return MetricService(MetricRepository(db))


@router.post("", response_model=MetricRead, status_code=status.HTTP_201_CREATED)
async def create_metric(
    data: MetricCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: MetricService = Depends(get_metric_service),
) -> MetricRead:
    metric = await service.create(user_id, data)
    return MetricRead.model_validate(metric)


@router.get("", response_model=MetricList)
async def list_metrics(
    metric_type: MetricType | None = None,
    limit: int = Query(default=50, le=200, gt=0),
    offset: int = Query(default=0, ge=0),
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: MetricService = Depends(get_metric_service),
) -> MetricList:
    items, total = await service.list(user_id, metric_type, limit, offset)
    return MetricList(items=[MetricRead.model_validate(item) for item in items], total=total)


@router.get("/{metric_id}", response_model=MetricRead)
async def get_metric(
    metric_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: MetricService = Depends(get_metric_service),
) -> MetricRead:
    metric = await service.get(user_id, metric_id)
    if metric is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return MetricRead.model_validate(metric)


@router.patch("/{metric_id}", response_model=MetricRead)
async def update_metric(
    metric_id: uuid.UUID,
    data: MetricUpdate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: MetricService = Depends(get_metric_service),
) -> MetricRead:
    metric = await service.update(user_id, metric_id, data)
    if metric is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return MetricRead.model_validate(metric)


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric(
    metric_id: uuid.UUID,
    user_id: uuid.UUID = Depends(get_current_user_id),
    service: MetricService = Depends(get_metric_service),
) -> None:
    deleted = await service.delete(user_id, metric_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
