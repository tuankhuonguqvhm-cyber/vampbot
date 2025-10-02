"""Политики."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.policies import PoliciesService
from repositories.policies_repo import PoliciesRepository

router = Router(name='policies')


@router.message(Command('policies'))
async def cmd_policies(message: Message, db, **kwargs) -> None:
    service = PoliciesService(PoliciesRepository(db))
    active = await service.active(message.from_user.id)
    if not active:
        await message.answer("Нет активных политик. Используйте промокоды или исследования, чтобы открыть новые.")
    else:
        await message.answer("Активные политики:
" + "
".join(f"• {code}" for code in active))
