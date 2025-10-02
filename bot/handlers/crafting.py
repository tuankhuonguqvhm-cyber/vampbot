"""Крафт."""
from __future__ import annotations

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from services.crafting import CraftingService

router = Router(name='crafting')


@router.message(Command('craft'))
async def cmd_craft(message: Message) -> None:
    crafting = CraftingService()
    recipes = "
".join(f"• {code} (стоимость {recipe.mats_cost}🧱)" for code, recipe in crafting.recipes.items())
    await message.answer("Доступные рецепты:
" + recipes)
