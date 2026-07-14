import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.metric import Metric, MetricType
from app.schemas.metric import MetricCreate, MetricUpdate


class MetricRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: uuid.UUID, data: MetricCreate) -> Metric:
        metric = Metric(
            user_id=user_id,
            metric_type=data.metric_type,
            value=data.value,
            recorded_at=data.recorded_at,
        )
        self._session.add(metric)
        await self._session.commit()
        await self._session.refresh(metric)
        return metric

    async def get(self, user_id: uuid.UUID, metric_id: uuid.UUID) -> Metric | None:
        result = await self._session.execute(
            select(Metric).where(Metric.id == metric_id, Metric.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        user_id: uuid.UUID,
        metric_type: MetricType | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[list[Metric], int]:
        filters = [Metric.user_id == user_id]
        if metric_type is not None:
            filters.append(Metric.metric_type == metric_type)

        total_result = await self._session.execute(
            select(func.count()).select_from(Metric).where(*filters)
        )
        total = total_result.scalar_one()

        items_result = await self._session.execute(
            select(Metric)
            .where(*filters)
            .order_by(Metric.recorded_at.desc())
            .limit(limit)
            .offset(offset)
        )
        items = list(items_result.scalars().all())
        return items, total

    async def update(
        self, user_id: uuid.UUID, metric_id: uuid.UUID, data: MetricUpdate
    ) -> Metric | None:
        metric = await self.get(user_id, metric_id)
        if metric is None:
            return None

        if data.value is not None:
            metric.value = data.value
        if data.recorded_at is not None:
            metric.recorded_at = data.recorded_at

        await self._session.commit()
        await self._session.refresh(metric)
        return metric

    async def delete(self, user_id: uuid.UUID, metric_id: uuid.UUID) -> bool:
        metric = await self.get(user_id, metric_id)
        if metric is None:
            return False

        await self._session.delete(metric)
        await self._session.commit()
        return True
