"""Главное меню."""
from __future__ import annotations

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='🏙️ Город'), KeyboardButton(text='🏗️ Строить')],
        [KeyboardButton(text='🔬 Исслед.'), KeyboardButton(text='🏛️ Политики')],
        [KeyboardButton(text='🎯 Квесты'), KeyboardButton(text='🏆 Рейтинги')],
        [KeyboardButton(text='🛒 Рынок'), KeyboardButton(text='🛡️ Дуэли')],
        [KeyboardButton(text='👥 Клан'), KeyboardButton(text='🧩 Крафт')],
        [KeyboardButton(text='🎁 Бонусы'), KeyboardButton(text='⚙️ Настройки')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
