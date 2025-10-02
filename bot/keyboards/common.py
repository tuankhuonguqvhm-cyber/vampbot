"""Общие клавиатуры."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def confirm_keyboard(callback_yes: str, callback_no: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='✅ Да', callback_data=callback_yes)],
            [InlineKeyboardButton(text='❌ Нет', callback_data=callback_no)],
        ]
    )
