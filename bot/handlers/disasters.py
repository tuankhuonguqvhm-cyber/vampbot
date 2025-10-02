"""Дизастеры."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.disasters import DisasterService

router = Router(name='disasters')


@router.message(Command('disasters'))
async def cmd_disaster(message: Message) -> None:
    service = DisasterService()
    event = service.roll()
    impact = ", ".join(f"{k}: {v}" for k, v in event.impact.items()) or "без последствий"
    await message.answer(f"Событие: {event.description}
Эффект: {impact}")
