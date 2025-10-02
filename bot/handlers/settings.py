"""Настройки."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name='settings')


@router.message(Command('settings'))
async def cmd_settings(message: Message) -> None:
    await message.answer("Настройки пока ограничены. Следите за обновлениями!")
