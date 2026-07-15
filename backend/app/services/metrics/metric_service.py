import uuid

from app.models.metric import Metric, MetricType
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate, MetricUpdate


class MetricService:
    def __init__(self, repository: MetricRepository) -> None:
        self._repository = repository

    async def create(self, user_id: uuid.UUID, data: MetricCreate) -> Metric:
        return await self._repository.create(user_id, data)

    async def get(self, user_id: uuid.UUID, metric_id: uuid.UUID) -> Metric | None:
        return await self._repository.get(user_id, metric_id)

    async def list(
        self, user_id: uuid.UUID, metric_type: MetricType | None, limit: int, offset: int
    ) -> tuple[list[Metric], int]:
        return await self._repository.list(user_id, metric_type, limit, offset)

    async def update(
        self, user_id: uuid.UUID, metric_id: uuid.UUID, data: MetricUpdate
    ) -> Metric | None:
        return await self._repository.update(user_id, metric_id, data)

    async def delete(self, user_id: uuid.UUID, metric_id: uuid.UUID) -> bool:
        return await self._repository.delete(user_id, metric_id)
