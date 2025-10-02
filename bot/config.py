"""Конфигурация приложения и загрузка переменных окружения."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(slots=True)
class BotConfig:
    """Параметры конфигурации Telegram-бота."""

    token: str
    admins: List[int]
    log_level: str
    database_path: Path


def load_config() -> BotConfig:
    """Загружает конфигурацию из переменных окружения."""

    token = os.getenv("BOT_TOKEN", "")
    if not token:
        raise RuntimeError("Не указан токен бота в переменной BOT_TOKEN")

    admin_raw = os.getenv("ADMIN_IDS", "")
    admins = [int(item.strip()) for item in admin_raw.split(",") if item.strip().isdigit()]
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    db_path = Path(os.getenv("DATABASE_PATH", "bot.db"))

    return BotConfig(
        token=token,
        admins=admins,
        log_level=log_level,
        database_path=db_path,
    )


CONFIG = load_config()
