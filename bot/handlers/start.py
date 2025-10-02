"""Обработчик команды /start."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from repositories.users_repo import UsersRepository
from repositories.cities_repo import CitiesRepository
from services.quests import QuestService
from repositories.quests_repo import QuestsRepository

router = Router(name='start')


@router.message(CommandStart())
async def cmd_start(message: Message, db, **kwargs) -> None:
    users = UsersRepository(db)
    cities = CitiesRepository(db)
    quests = QuestService(QuestsRepository(db))
    user = await users.get_or_create(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await quests.assign_daily(user['tg_id'])
    city = await cities.get(user.get('city_id', 1) or 1)
    await message.answer(
        "<b>Добро пожаловать в Городской Рывок+</b>!
"
        f"Ваш стартовый город: {city['emoji']} {city['name']}.
"
        "Используйте /menu для открытия основного меню."
    )
