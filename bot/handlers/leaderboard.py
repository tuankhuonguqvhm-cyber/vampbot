"""Рейтинги."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.leaderboard import LeaderboardService
from repositories.leaderboard_repo import LeaderboardRepository

router = Router(name='leaderboard')


@router.message(Command('top'))
async def cmd_top(message: Message, db, **kwargs) -> None:
    service = LeaderboardService(LeaderboardRepository(db))
    top = await service.top_prestige(10)
    if not top:
        await message.answer("Рейтинг пока пуст.")
    else:
        lines = ["🏆 Топ игроков:"]
        for idx, row in enumerate(top, start=1):
            lines.append(f"{idx}) @{row['username']} — {row['score']} ⭐")
        await message.answer("
".join(lines))
