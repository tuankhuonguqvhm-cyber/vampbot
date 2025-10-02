"""Кастомные мидлвари."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import timedelta
from typing import Any, Callable, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from config import BotConfig
from core.security import IdempotencyService, RateLimiter
from core.utils import now_utc

LOGGER = logging.getLogger(__name__)


@dataclass
class Context:
    db: Any
    scheduler: Any


class LoggingMiddleware(BaseMiddleware):
    """Логирует апдейты."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        LOGGER.debug("Update: %s", event)
        return await handler(event, data)


class IdempotencyMiddleware(BaseMiddleware):
    """Фильтрует повторные callback-и по nonce."""

    def __init__(self, service: IdempotencyService) -> None:
        self.service = service

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, CallbackQuery):
            nonce = None
            if event.data and "|" in event.data:
                parts = event.data.split("|")
                if len(parts) >= 4:
                    nonce = parts[-1]
            if nonce and not await self.service.register_nonce(nonce):
                await event.answer("Действие уже выполняется", show_alert=False)
                return None
        return await handler(event, data)


class RateLimitMiddleware(BaseMiddleware):
    """Rate limit по действиям пользователя."""

    def __init__(self, limiter: RateLimiter) -> None:
        self.limiter = limiter

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None
        action = "message"
        if isinstance(event, Message):
            user_id = event.from_user.id if event.from_user else None
            action = event.text or event.get_command() or "message"
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id if event.from_user else None
            action = event.data or "callback"
        if user_id and not await self.limiter.check(user_id, action):
            if isinstance(event, CallbackQuery):
                await event.answer("Слишком часто, подождите пару секунд", show_alert=True)
            else:
                await event.answer("Слишком часто, подождите пару секунд")
            return None
        return await handler(event, data)


class UserContextMiddleware(BaseMiddleware):
    """Загружает пользователя из базы и кладёт в контекст."""

    def __init__(self, db) -> None:
        self.db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = None
        if isinstance(event, (Message, CallbackQuery)):
            tg_user = event.from_user
            if tg_user:
                user_id = tg_user.id
        if user_id:
            data.setdefault("user_id", user_id)
        data.setdefault("db", self.db)
        return await handler(event, data)


def setup_middlewares(dp, db, config: BotConfig, scheduler) -> None:
    """Регистрирует все мидлвари."""

    idem_service = IdempotencyService(db)
    rate_limiter = RateLimiter(db, cooldown=timedelta(seconds=2))
    dp.update.middleware(LoggingMiddleware())
    dp.update.middleware(IdempotencyMiddleware(idem_service))
    dp.update.middleware(RateLimitMiddleware(rate_limiter))
    dp.update.middleware(UserContextMiddleware(db))
