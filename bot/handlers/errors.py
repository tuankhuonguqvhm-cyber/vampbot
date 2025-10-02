"""Глобальный обработчик ошибок."""
from __future__ import annotations

import logging

from aiogram import Router
from aiogram.types import ErrorEvent

router = Router(name='errors')
LOGGER = logging.getLogger(__name__)


@router.errors()
async def handle_error(event: ErrorEvent) -> None:
    LOGGER.exception("Unhandled error: %s", event.exception)
