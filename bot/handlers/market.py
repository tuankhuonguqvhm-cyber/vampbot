"""Рынок."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.market import MarketService
from repositories.market_repo import MarketRepository

router = Router(name='market')


@router.message(Command('market'))
async def cmd_market(message: Message, db, **kwargs) -> None:
    service = MarketService(MarketRepository(db))
    order_id = await service.create_order(message.from_user.id, 'sell', 'mats', 10, 100)
    price = await service.recommended_price('mats', 100.0)
    await message.answer(f"Создан ордер #{order_id}. Рекомендуемая цена сейчас {price:.2f}💰 за единицу.")
