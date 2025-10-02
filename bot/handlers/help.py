"""Подсказка."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.texts import HELP_TEXT

router = Router(name='help')


@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)
