LLM Telegram Platform
Описание проекта

Проект представляет собой микросервисную систему для работы Telegram-бота с LLM-моделью через OpenRouter.

Система состоит из двух независимых сервисов:

auth_service — отвечает за регистрацию, логин и выпуск JWT-токенов.
bot_service — Telegram-бот на aiogram, принимающий JWT и выполняющий запросы к LLM через асинхронную очередь задач.
Архитектура
Telegram User
      ↓
Bot Service (aiogram)
      ↓
JWT validation
      ↓
RabbitMQ
      ↓
Celery Worker
      ↓
OpenRouter API
      ↓
Telegram response

Redis используется для хранения JWT, привязанных к Telegram user_id.

RabbitMQ используется как брокер задач Celery.