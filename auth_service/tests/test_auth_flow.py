import pytest
from httpx import ASGITransport, AsyncClient

from app.db.base import Base
from app.db.session import engine
from app.main import app


@pytest.mark.asyncio
async def test_auth_full_flow():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        register_response = await client.post(
            "/auth/register",
            json={
                "email": "ivan@example.com",
                "password": "12345678"
            }
        )

        assert register_response.status_code == 201

        register_data = register_response.json()

        assert register_data["email"] == "ivan@example.com"
        assert register_data["role"] == "user"
        assert "password_hash" not in register_data

        login_response = await client.post(
            "/auth/login",
            data={
                "username": "ivan@example.com",
                "password": "12345678"
            }
        )

        assert login_response.status_code == 200

        login_data = login_response.json()

        assert "access_token" in login_data
        assert login_data["token_type"] == "bearer"

        token = login_data["access_token"]

        me_response = await client.get(
            "/auth/me",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert me_response.status_code == 200

        me_data = me_response.json()

        assert me_data["email"] == "ivan@example.com"
        assert me_data["role"] == "user"
        assert "password_hash" not in me_data