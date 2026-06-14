from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request


router = Router()


@router.message(Command("start"))
async def start_handler(
    message: Message,
) -> None:
    await message.answer(
        "Привет. Сначала отправь JWT-токен командой:\n\n"
        "/token <твой_jwt_токен>\n\n"
        "Токен можно получить в Auth Service через /auth/login."
    )


@router.message(Command("token"))
async def token_handler(
    message: Message,
) -> None:
    user_id = message.from_user.id

    command_text = message.text or ""
    parts = command_text.split(maxsplit=1)

    if len(parts) != 2:
        await message.answer(
            "Нужно отправить токен так:\n\n"
            "/token <твой_jwt_токен>"
        )
        return

    token = parts[1].strip()

    try:
        decode_and_validate(token)

    except ValueError:
        await message.answer(
            "Токен неверный или истёк. "
            "Получи новый токен в Auth Service."
        )
        return

    redis_client = get_redis()

    await redis_client.set(
        name=f"token:{user_id}",
        value=token,
    )

    await message.answer(
        "Токен принят и сохранён. Теперь можешь отправлять вопросы."
    )


@router.message(F.text)
async def text_handler(
    message: Message,
) -> None:
    user_id = message.from_user.id
    chat_id = message.chat.id
    prompt = message.text

    redis_client = get_redis()

    token = await redis_client.get(
        f"token:{user_id}"
    )

    if token is None:
        await message.answer(
            "У тебя нет сохранённого JWT-токена.\n\n"
            "Сначала авторизуйся в Auth Service и отправь токен командой:\n"
            "/token <твой_jwt_токен>"
        )
        return

    try:
        decode_and_validate(token)

    except ValueError:
        await message.answer(
            "Твой токен неверный или истёк.\n\n"
            "Получи новый токен в Auth Service и отправь его командой:\n"
            "/token <твой_jwt_токен>"
        )
        return

    llm_request.delay(
        tg_chat_id=chat_id,
        prompt=prompt,
    )

    await message.answer(
        "Запрос принят. Ответ обрабатывается подождите..."
    )