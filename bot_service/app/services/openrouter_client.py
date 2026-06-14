import httpx

from app.core.config import settings


async def call_openrouter(
    prompt: str,
) -> str:

    url = (
        f"{settings.OPENROUTER_BASE_URL}"
        "/chat/completions"
    )

    headers = {
        "Authorization": (
            f"Bearer {settings.OPENROUTER_API_KEY}"
        ),
        "HTTP-Referer": (
            settings.OPENROUTER_SITE_URL
        ),
        "X-Title": (
            settings.OPENROUTER_APP_NAME
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    try:
        async with httpx.AsyncClient(
            timeout=60.0
        ) as client:

            response = await client.post(
                url=url,
                headers=headers,
                json=payload,
            )

    except httpx.ConnectError:
        raise RuntimeError(
            "Failed to connect to OpenRouter"
        )

    except httpx.TimeoutException:
        raise RuntimeError(
            "OpenRouter request timeout"
        )

    except httpx.HTTPError as error:
        raise RuntimeError(
            f"OpenRouter HTTP error: {error}"
        )

    if response.status_code != 200:
        raise RuntimeError(
            "OpenRouter returned non-200 response: "
            f"{response.status_code} "
            f"{response.text}"
        )

    data = response.json()

    try:
        answer = data["choices"][0]["message"]["content"]

    except (
        KeyError,
        IndexError,
        TypeError,
    ):
        raise RuntimeError(
            "Invalid OpenRouter response format"
        )

    return answer