"""Достижения."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.achievements import AchievementService
from repositories.achievements_repo import AchievementsRepository

router = Router(name='achievements')


@router.message(Command('achievements'))
async def cmd_achievements(message: Message, db, **kwargs) -> None:
    service = AchievementService(AchievementsRepository(db))
    progress = await service.progress(message.from_user.id)
    if not progress:
        await message.answer("У вас пока нет достижений. Выполняйте квесты и развивайте город!")
    else:
        preview = list(progress.items())[:5]
        text = "Ваши достижения:
" + "
".join(f"• {code}: {data['progress']}" for code, data in preview)
        await message.answer(text)
