import pytest
from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.fixture
async def client():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as async_client:
        yield async_client


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(
    client: AsyncClient,
):
    payload = {
        "email": "ivan@example.com",
        "password": "12345678",
    }

    first_response = await client.post(
        "/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = await client.post(
        "/auth/register",
        json=payload,
    )

    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_wrong_password_returns_401(
    client: AsyncClient,
):
    register_response = await client.post(
        "/auth/register",
        json={
            "email": "ivan@example.com",
            "password": "12345678",
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        data={
            "username": "ivan@example.com",
            "password": "wrong_password",
        },
    )

    assert login_response.status_code == 401


@pytest.mark.asyncio
async def test_me_without_token_returns_401(
    client: AsyncClient,
):
    response = await client.get(
        "/auth/me"
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_me_with_invalid_token_returns_401(
    client: AsyncClient,
):
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid_token",
        },
    )

    assert response.status_code == 401