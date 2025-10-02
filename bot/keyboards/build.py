"""Заглушка клавиатуры."""
from __future__ import annotations

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def placeholder_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='⬅️ Назад')]], resize_keyboard=True)
