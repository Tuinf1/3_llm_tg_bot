from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    InvalidTokenError,
    TokenExpiredError,
    UserNotFoundError,
)
from app.core.security import decode_token
from app.db.session import AsyncSessionLocal
from app.repositories.users import UsersRepository
from app.usecases.auth import AuthUseCase




oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_users_repo(
    session: AsyncSession = Depends(get_db)
) -> UsersRepository:
    return UsersRepository(session=session)


def get_auth_uc(
    users_repository: UsersRepository = Depends(get_users_repo)
) -> AuthUseCase:
    return AuthUseCase(
        users_repository=users_repository
    )


async def get_current_user_id(
    token: str = Depends(oauth2_scheme)
) -> int:

    try:
        payload = decode_token(token)

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except JWTError:
        raise InvalidTokenError()

    except ValueError:
        raise InvalidTokenError()

    user_id = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError()

    return int(user_id)


async def get_current_user(
    user_id: int = Depends(get_current_user_id),
    auth_uc: AuthUseCase = Depends(get_auth_uc)
):
    user = await auth_uc.me(
        user_id=user_id
    )

    if user is None:
        raise UserNotFoundError()

    return user