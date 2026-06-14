import asyncio

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter


async def send_telegram_message(
    tg_chat_id: int,
    text: str,
) -> None:
    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN
    )

    try:
        await bot.send_message(
            chat_id=tg_chat_id,
            text=text,
        )

    finally:
        await bot.session.close()


async def process_llm_request(
    tg_chat_id: int,
    prompt: str,
) -> None:
    try:
        answer = await call_openrouter(
            prompt=prompt
        )

    except Exception as error:
        answer = (
            "Не удалось получить ответ от LLM. "
            f"Ошибка: {error}"
        )

    await send_telegram_message(
        tg_chat_id=tg_chat_id,
        text=answer,
    )


@celery_app.task(
    name="app.tasks.llm_tasks.llm_request"
)
def llm_request(
    tg_chat_id: int,
    prompt: str,
) -> dict:
    asyncio.run(
        process_llm_request(
            tg_chat_id=tg_chat_id,
            prompt=prompt,
        )
    )

    return {
        "status": "sent",
        "tg_chat_id": tg_chat_id,
    }

