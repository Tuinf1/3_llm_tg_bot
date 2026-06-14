import fakeredis.aioredis
import pytest

from app.bot import handlers


@pytest.fixture
async def fake_redis():
    redis_client = fakeredis.aioredis.FakeRedis(
        decode_responses=True
    )

    await redis_client.flushall()

    yield redis_client

    await redis_client.flushall()
    await redis_client.aclose()


@pytest.fixture(autouse=True)
async def patch_redis(
    monkeypatch,
    fake_redis,
):
    monkeypatch.setattr(
        handlers,
        "get_redis",
        lambda: fake_redis,
    )

    yield