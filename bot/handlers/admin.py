"""Административные команды."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.filters import AdminFilter

router = Router(name='admin')
router.message.filter(AdminFilter([]))


@router.message(Command('admin'))
async def cmd_admin(message: Message) -> None:
    await message.answer("Админский режим активен. Здесь будут настройки и отчёты.")
