"""Квесты."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.quests import QuestService
from repositories.quests_repo import QuestsRepository

router = Router(name='quests')


@router.message(Command('quests'))
async def cmd_quests(message: Message, db, **kwargs) -> None:
    service = QuestService(QuestsRepository(db))
    quests = await service.list(message.from_user.id)
    if not quests:
        await message.answer("Квесты ещё не назначены. Загляните позже.")
        return
    lines = ["Активные квесты:"]
    for q in quests:
        lines.append(f"• {q['quest_code']} — прогресс {q['progress']}")
    await message.answer("
".join(lines))
