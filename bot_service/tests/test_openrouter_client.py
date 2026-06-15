import pytest
import respx
from httpx import Response

from app.core.config import settings
from app.services.openrouter_client import call_openrouter


@pytest.mark.asyncio
@respx.mock
async def test_call_openrouter_returns_answer():
    route = respx.post(
        f"{settings.OPENROUTER_BASE_URL}/chat/completions"
    ).mock(
        return_value=Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": "Тестовый ответ LLM"
                        }
                    }
                ]
            },
        )
    )

    answer = await call_openrouter(
        prompt="Привет"
    )

    assert answer == "Тестовый ответ LLM"
    assert route.called