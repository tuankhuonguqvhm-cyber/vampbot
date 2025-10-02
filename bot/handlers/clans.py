"""Кланы."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.clans import ClanService
from repositories.clans_repo import ClansRepository

router = Router(name='clans')


@router.message(Command('clan'))
async def cmd_clan(message: Message, db, **kwargs) -> None:
    service = ClanService(ClansRepository(db))
    info = await service.info(1)
    members = "
".join(f"• {m['user_id']} — {m['role']}" for m in info.members) or "Пока пусто"
    await message.answer(f"Клан {info.tag}
Участники:
{members}")
