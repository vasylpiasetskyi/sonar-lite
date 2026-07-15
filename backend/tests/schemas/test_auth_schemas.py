import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.schemas.auth import AuthResponse, UserCreate, UserRead


def test_user_create_accepts_valid_email_and_password() -> None:
    user = UserCreate(email="person@example.com", password="longenough")
    assert user.email == "person@example.com"


def test_user_create_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="longenough")


def test_user_create_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="person@example.com", password="short")


def test_user_create_rejects_password_over_72_chars() -> None:
    with pytest.raises(ValidationError):
        UserCreate(email="person@example.com", password="a" * 73)


def test_auth_response_defaults_token_type_to_bearer() -> None:
    response = AuthResponse(
        user=UserRead(
            id=uuid.uuid4(), email="person@example.com", created_at=datetime.now(timezone.utc)
        ),
        access_token="abc.def.ghi",
    )
    assert response.token_type == "bearer"
