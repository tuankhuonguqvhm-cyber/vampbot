"""Мастер строительства."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from repositories.buildings_repo import BuildingsRepository
from repositories.inventory_repo import InventoryRepository
from repositories.users_repo import UsersRepository
from services.buildings import BuildingService

router = Router(name='build')


@router.message(Command('build'))
async def cmd_build(message: Message, db, **kwargs) -> None:
    service = BuildingService(BuildingsRepository(db), InventoryRepository(db), UsersRepository(db))
    result = await service.start_build(message.from_user.id, 'BLD_001', 1)
    await message.answer(result.message)
