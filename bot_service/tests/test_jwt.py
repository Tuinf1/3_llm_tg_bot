from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.core.config import settings
from app.core.jwt import decode_and_validate


def test_decode_and_validate_valid_token():
    now = datetime.now(timezone.utc)

    payload = {
        "sub": "1",
        "role": "user",
        "iat": int(now.timestamp()),
        "exp": now + timedelta(minutes=10),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )

    decoded_payload = decode_and_validate(token)

    assert decoded_payload["sub"] == "1"
    assert decoded_payload["role"] == "user"


def test_decode_and_validate_invalid_token():
    with pytest.raises(ValueError):
        decode_and_validate("invalid_token")