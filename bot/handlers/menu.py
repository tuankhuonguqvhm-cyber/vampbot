"""Главное меню."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.menu import main_menu

router = Router(name='menu')


@router.message(Command('menu'))
async def cmd_menu(message: Message) -> None:
    await message.answer("Выберите действие:", reply_markup=main_menu())
