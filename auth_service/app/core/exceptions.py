from fastapi import HTTPException


class BaseHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str
    ):
        super().__init__(
            status_code=status_code,
            detail=detail
        )


class UserAlreadyExistsError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=409,
            detail="User already exists"
        )


class InvalidCredentialsError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid credentials"
        )


class InvalidTokenError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Invalid token"
        )


class TokenExpiredError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Token expired"
        )


class UserNotFoundError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="User not found"
        )


class PermissionDeniedError(BaseHTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Permission denied"
        )