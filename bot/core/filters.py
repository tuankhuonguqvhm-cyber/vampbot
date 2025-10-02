"""Дополнительные фильтры aiogram."""
from __future__ import annotations

from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class AdminFilter(BaseFilter):
    def __init__(self, admin_ids: list[int]) -> None:
        self.admin_ids = admin_ids

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        user = obj.from_user
        return bool(user and user.id in self.admin_ids)


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str) -> None:
        self.chat_type = chat_type

    async def __call__(self, obj: Message | CallbackQuery) -> bool:
        chat = obj.chat if isinstance(obj, Message) else obj.message.chat if obj.message else None
        return bool(chat and chat.type == self.chat_type)
