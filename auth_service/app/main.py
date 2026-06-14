from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import router as api_router
from app.db.base import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="Auth Service",
    description="Service for user registration, login and JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "auth_service",
    }


app.include_router(api_router)