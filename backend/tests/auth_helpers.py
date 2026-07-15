import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.services.auth.auth_service import AuthService


async def create_test_user_token(db_session: AsyncSession) -> str:
    service = AuthService(UserRepository(db_session))
    email = f"test-{uuid.uuid4()}@example.com"
    _, token = await service.register(email, "test-password-123")
    return token


async def create_test_user_id(db_session: AsyncSession) -> uuid.UUID:
    repo = UserRepository(db_session)
    email = f"test-{uuid.uuid4()}@example.com"
    user = await repo.create(email, "test-password-hash")
    return user.id
