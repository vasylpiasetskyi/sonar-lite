import pytest

from app.repositories.user_repository import UserRepository
from app.services.auth.auth_service import (
    AuthService,
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
)


async def test_register_creates_user_and_returns_token(db_session) -> None:
    service = AuthService(UserRepository(db_session))

    user, token = await service.register("person@example.com", "longenough")

    assert user.email == "person@example.com"
    assert token


async def test_register_rejects_duplicate_email(db_session) -> None:
    service = AuthService(UserRepository(db_session))
    await service.register("person@example.com", "longenough")

    with pytest.raises(EmailAlreadyRegisteredError):
        await service.register("person@example.com", "different-password")


async def test_authenticate_succeeds_with_correct_password(db_session) -> None:
    service = AuthService(UserRepository(db_session))
    await service.register("person@example.com", "longenough")

    user, token = await service.authenticate("person@example.com", "longenough")

    assert user.email == "person@example.com"
    assert token


async def test_authenticate_rejects_wrong_password(db_session) -> None:
    service = AuthService(UserRepository(db_session))
    await service.register("person@example.com", "longenough")

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate("person@example.com", "wrong-password")


async def test_authenticate_rejects_unknown_email(db_session) -> None:
    service = AuthService(UserRepository(db_session))

    with pytest.raises(InvalidCredentialsError):
        await service.authenticate("nobody@example.com", "whatever")
