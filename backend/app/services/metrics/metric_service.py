import uuid

from app.core.constants import DEMO_USER_ID
from app.models.metric import Metric, MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate, MetricUpdate


class MetricService:
    def __init__(self, repository: MetricRepository) -> None:
        self._repository = repository

    async def create(self, data: MetricCreate) -> Metric:
        return await self._repository.create(DEMO_USER_ID, data)

    async def get(self, metric_id: uuid.UUID) -> Metric | None:
        return await self._repository.get(DEMO_USER_ID, metric_id)

    async def list(
        self, metric_type: MetricType | None, limit: int, offset: int
    ) -> tuple[list[Metric], int]:
        return await self._repository.list(DEMO_USER_ID, metric_type, limit, offset)

    async def update(self, metric_id: uuid.UUID, data: MetricUpdate) -> Metric | None:
        return await self._repository.update(DEMO_USER_ID, metric_id, data)

    async def delete(self, metric_id: uuid.UUID) -> bool:
        return await self._repository.delete(DEMO_USER_ID, metric_id)
