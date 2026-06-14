
from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)



from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)



from app.db.models import User
from app.repositories.users import UsersRepository
from app.schemas.auth import RegisterRequest, TokenResponse




class AuthUseCase:


    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository



    async def register(
        self,
        data: RegisterRequest
    ) -> User:

        existing_user = await self.users_repository.get_by_email(
            email=data.email
        )

        if existing_user is not None:
            raise UserAlreadyExistsError()

        password_hash = hash_password(
            password=data.password
        )

        user = await self.users_repository.create(
            email=data.email,
            password_hash=password_hash,
            role="user"
        )

        return user


    async def login(
        self,
        email: str,
        password: str
    ) -> TokenResponse:

        user = await self.users_repository.get_by_email(
            email=email
        )

        if user is None:
            raise InvalidCredentialsError()

        password_is_valid = verify_password(
            password=password,
            password_hash=user.password_hash
        )

        if not password_is_valid:
            raise InvalidCredentialsError()

        access_token = create_access_token(
            user_id=user.id,
            role=user.role
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )



    async def me(
        self,
        user_id: int
    ) -> User:

        user = await self.users_repository.get_by_id(
            user_id=user_id
        )

        if user is None:
            raise UserNotFoundError()

        return user
    
