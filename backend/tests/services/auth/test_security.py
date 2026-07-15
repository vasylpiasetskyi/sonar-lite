import uuid
from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core.config import settings
from app.services.auth.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password_produces_a_verifiable_hash() -> None:
    hashed = hash_password("correct-horse-battery-staple")

    assert verify_password("correct-horse-battery-staple", hashed) is True


def test_verify_password_rejects_wrong_password() -> None:
    hashed = hash_password("correct-horse-battery-staple")

    assert verify_password("wrong-password", hashed) is False


def test_create_and_decode_access_token_round_trips_user_id() -> None:
    user_id = uuid.uuid4()

    token = create_access_token(user_id)
    decoded_user_id = decode_access_token(token)

    assert decoded_user_id == user_id


def test_decode_access_token_rejects_expired_token() -> None:
    expired_payload = {
        "sub": str(uuid.uuid4()),
        "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
    }
    expired_token = jwt.encode(
        expired_payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_access_token(expired_token)


def test_decode_access_token_rejects_tampered_token() -> None:
    # Tamper a character in the interior of the payload segment, not its last
    # character — trailing base64url characters can have unused ("don't
    # care") bits, so flipping the very last char occasionally decodes to
    # the same underlying bytes and leaves the signature valid (flaky test).
    token = create_access_token(uuid.uuid4())
    header, payload, signature = token.split(".")
    tampered_char = "A" if payload[5] != "A" else "B"
    tampered_payload = payload[:5] + tampered_char + payload[6:]
    tampered_token = f"{header}.{tampered_payload}.{signature}"

    with pytest.raises(jwt.InvalidTokenError):
        decode_access_token(tampered_token)
