"""Крафт и переработка."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class CraftRecipe:
    code: str
    mats_cost: int
    energy_cost: int
    reward: Dict[str, int]


class CraftingService:
    def __init__(self) -> None:
        self.recipes = {
            'recycle': CraftRecipe('recycle', 50, 10, {'money': 200}),
            'upgrade': CraftRecipe('upgrade', 120, 20, {'prestige': 5}),
        }

    def get(self, code: str) -> CraftRecipe | None:
        return self.recipes.get(code)
