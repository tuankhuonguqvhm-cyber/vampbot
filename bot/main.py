"""Точка входа Telegram-бота «Городской Рывок+»."""
from __future__ import annotations

import asyncio
import logging
from typing import Sequence

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import CONFIG
from core.db import Database
from core.middlewares import setup_middlewares
from handlers import (
    start,
    menu,
    city,
    build,
    research as research_handler,
    policies as policies_handler,
    quests as quests_handler,
    achievements as achievements_handler,
    disasters as disasters_handler,
    clans as clans_handler,
    market as market_handler,
    crafting as crafting_handler,
    duels as duels_handler,
    referrals as referrals_handler,
    leaderboard as leaderboard_handler,
    inline as inline_handler,
    settings as settings_handler,
    admin as admin_handler,
    help as help_handler,
    errors as errors_handler,
)
from services.scheduler import SchedulerService


async def register_handlers(dp: Dispatcher) -> None:
    """Регистрирует все обработчики в диспетчере."""

    routers: Sequence = [
        start.router,
        menu.router,
        city.router,
        build.router,
        research_handler.router,
        policies_handler.router,
        quests_handler.router,
        achievements_handler.router,
        disasters_handler.router,
        clans_handler.router,
        market_handler.router,
        crafting_handler.router,
        duels_handler.router,
        referrals_handler.router,
        leaderboard_handler.router,
        inline_handler.router,
        settings_handler.router,
        admin_handler.router,
        help_handler.router,
        errors_handler.router,
    ]
    for router in routers:
        dp.include_router(router)


async def main() -> None:
    """Основная асинхронная функция запуска бота."""

    logging.basicConfig(level=getattr(logging, CONFIG.log_level, logging.INFO))
    logger = logging.getLogger(__name__)
    logger.info("Запуск бота с уровнем логирования %s", CONFIG.log_level)

    storage = MemoryStorage()
    bot = Bot(token=CONFIG.token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=storage)

    db = Database(CONFIG.database_path)
    await db.setup()

    scheduler = SchedulerService(db=db, bot=bot)
    await scheduler.start()

    setup_middlewares(dp, db=db, config=CONFIG, scheduler=scheduler)
    await register_handlers(dp)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await scheduler.stop()
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())
