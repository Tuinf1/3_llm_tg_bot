from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, ExpiredSignatureError, jwt
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return password_context.verify(password, password_hash)


def create_access_token(
    user_id: int,
    role: str
) -> str:
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload: dict[str, Any] = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": expire,
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG
    )

    return token


def decode_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG]
        )

        return payload

    except ExpiredSignatureError:
        raise ValueError("Token expired")

    except JWTError:
        raise ValueError("Invalid token")

