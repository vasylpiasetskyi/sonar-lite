import uuid

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security_deps import get_current_user_id
from app.services.auth.security import create_access_token


def test_get_current_user_id_returns_user_id_for_valid_token() -> None:
    user_id = uuid.uuid4()
    token = create_access_token(user_id)
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)

    result = get_current_user_id(credentials)

    assert result == user_id


def test_get_current_user_id_raises_401_for_missing_credentials() -> None:
    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(None)

    assert exc_info.value.status_code == 401


def test_get_current_user_id_raises_401_for_invalid_token() -> None:
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="not-a-real-token")

    with pytest.raises(HTTPException) as exc_info:
        get_current_user_id(credentials)

    assert exc_info.value.status_code == 401
