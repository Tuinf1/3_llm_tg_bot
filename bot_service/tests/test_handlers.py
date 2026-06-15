from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest
from jose import jwt

from app.bot.handlers import text_handler, token_handler
from app.core.config import settings


class FakeMessage:
    def __init__(
        self,
        text: str,
        user_id: int = 100,
        chat_id: int = 200,
    ):
        self.text = text
        self.from_user = SimpleNamespace(id=user_id)
        self.chat = SimpleNamespace(id=chat_id)
        self.answers = []

    async def answer(
        self,
        text: str,
    ):
        self.answers.append(text)


def make_token(
    user_id: int = 1,
    role: str = "user",
) -> str:
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "role": role,
        "iat": int(now.timestamp()),
        "exp": now + timedelta(minutes=10),
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALG,
    )


@pytest.mark.asyncio
async def test_token_command_saves_token_to_redis(
    fake_redis,
):
    token = make_token()

    message = FakeMessage(
        text=f"/token {token}",
        user_id=100,
        chat_id=200,
    )

    await token_handler(message)

    saved_token = await fake_redis.get(
        "token:100"
    )

    assert saved_token == token
    assert "Токен принят" in message.answers[0]


@pytest.mark.asyncio
async def test_text_without_token_does_not_call_celery(
    mocker,
):
    delay_mock = mocker.patch(
        "app.bot.handlers.llm_request.delay"
    )

    message = FakeMessage(
        text="Привет",
        user_id=100,
        chat_id=200,
    )

    await text_handler(message)

    delay_mock.assert_not_called()
    assert "нет сохранённого JWT-токена" in message.answers[0]


@pytest.mark.asyncio
async def test_text_with_token_calls_celery(
    fake_redis,
    mocker,
):
    token = make_token()

    await fake_redis.set(
        "token:100",
        token,
    )

    delay_mock = mocker.patch(
        "app.bot.handlers.llm_request.delay"
    )

    message = FakeMessage(
        text="Привет",
        user_id=100,
        chat_id=200,
    )

    await text_handler(message)

    delay_mock.assert_called_once_with(
        tg_chat_id=200,
        prompt="Привет",
    )

    assert "Запрос принят" in message.answers[0]