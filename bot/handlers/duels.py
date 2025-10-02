"""Дуэли."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.duels import DuelService

router = Router(name='duels')
_duels = DuelService()


@router.message(Command('duel'))
async def cmd_duel(message: Message) -> None:
    duel = _duels.create(message.from_user.id, 1, 100)
    await message.answer(f"Вы бросили вызов игроку {duel.opponent_id} со ставкой {duel.wager}💰. Код дуэли: {duel.id}")
