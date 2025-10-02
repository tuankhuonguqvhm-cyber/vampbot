"""Рефералы."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.referrals import ReferralService
from repositories.referrals_repo import ReferralsRepository

router = Router(name='referrals')


@router.message(Command('referrals'))
async def cmd_referrals(message: Message, db, **kwargs) -> None:
    service = ReferralService(ReferralsRepository(db))
    ok = await service.activate(message.from_user.id, 'REF1')
    await message.answer("Реферальный код активирован" if ok else "Реферальный код недоступен")
