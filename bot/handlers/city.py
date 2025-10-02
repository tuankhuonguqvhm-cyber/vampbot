"""Сводка города."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from repositories.users_repo import UsersRepository
from repositories.cities_repo import CitiesRepository
from services.ticks import TickService
from repositories.inventory_repo import InventoryRepository
from repositories.buildings_repo import BuildingsRepository
from repositories.policies_repo import PoliciesRepository
from repositories.research_repo import ResearchRepository
from core.texts import city_summary
from services.seasons import SeasonsService
from repositories.seasons_repo import SeasonsRepository

router = Router(name='city')


@router.message(Command('city'))
async def cmd_city(message: Message, db, **kwargs) -> None:
    users = UsersRepository(db)
    cities = CitiesRepository(db)
    inventory = InventoryRepository(db)
    buildings = BuildingsRepository(db)
    policies = PoliciesRepository(db)
    research = ResearchRepository(db)
    ticks = TickService(users, inventory, buildings, policies, research)
    seasons = SeasonsService(SeasonsRepository(db))
    user = await users.get_or_create(message.from_user.id, message.from_user.username, message.from_user.first_name)
    result = await ticks.perform_tick(user['tg_id'])
    city = await cities.get(user.get('city_id', 1) or 1)
    incomes = {
        'money': result.money_delta // max(result.minutes, 1),
        'mats': result.mats_delta // max(result.minutes, 1),
        'energy': result.energy_delta // max(result.minutes, 1),
    }
    text = city_summary({**user, 'mult': 1.0}, city, seasons.current_index(), incomes)
    await message.answer(text)
