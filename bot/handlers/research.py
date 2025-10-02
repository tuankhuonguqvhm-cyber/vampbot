"""Исследования."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.research import ResearchService
from repositories.research_repo import ResearchRepository

router = Router(name='research')


@router.message(Command('research'))
async def cmd_research(message: Message, db, **kwargs) -> None:
    service = ResearchService(ResearchRepository(db))
    tree = await service.tree(message.from_user.id)
    if not tree:
        await message.answer("Исследований пока нет. Попробуйте начать базовое исследование.")
    else:
        lines = ["Ваши исследования:"]
        for code, level in tree.items():
            lines.append(f"• {code} — уровень {level}")
        await message.answer("
".join(lines))
