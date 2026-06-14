from typing import Any

from jose import ExpiredSignatureError, JWTError, jwt

from app.core.config import settings


def decode_and_validate(
    token: str
) -> dict[str, Any]:

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )

    except ExpiredSignatureError:
        raise ValueError("Token expired")

    except JWTError:
        raise ValueError("Invalid token")

    user_id = payload.get("sub")

    if user_id is None:
        raise ValueError("Token has no subject")

    return payload