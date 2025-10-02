"""Фоновые задачи."""
from __future__ import annotations

import asyncio
import logging
from typing import Optional

from aiogram import Bot

from core.utils import now_utc

LOGGER = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self, db, bot: Bot) -> None:
        self.db = db
        self.bot = bot
        self._task: Optional[asyncio.Task] = None
        self._stop = asyncio.Event()

    async def start(self) -> None:
        if self._task:
            return
        self._stop.clear()
        self._task = asyncio.create_task(self._loop())

    async def stop(self) -> None:
        if not self._task:
            return
        self._stop.set()
        await self._task
        self._task = None

    async def _loop(self) -> None:
        while not self._stop.is_set():
            LOGGER.debug("Scheduler heartbeat %s", now_utc())
            await asyncio.sleep(60)
