"""Модели и константы игрового баланса."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(slots=True)
class ResourcePack:
    """Описание ресурса."""

    money: int = 0
    mats: int = 0
    energy: int = 0
    prestige: int = 0


@dataclass(slots=True)
class BuildingLevel:
    level: int
    money: int
    mats: int
    time_minutes: int
    income_money: int
    income_mats: int
    income_energy: int


@dataclass(slots=True)
class BuildingType:
    code: str
    name: str
    category: str
    description: str
    base_cost_money: int
    base_cost_mats: int
    base_energy: int
    base_income_money: int
    base_income_mats: int
    base_income_energy: int
    growth_cost: float
    growth_income: float
    requires: Dict[str, List[str] | int]
    modules: List[Dict[str, str | float]]
    levels: List[BuildingLevel]


@dataclass(slots=True)
class QuestTemplate:
    code: str
    text: str
    kind: str
    target: int
    reward: ResourcePack


@dataclass(slots=True)
class AchievementTemplate:
    code: str
    name: str
    category: str
    description: str
    threshold: int
    reward: ResourcePack
    title: Optional[str] = None


MAX_ENERGY: int = 100
ENERGY_REGEN_PER_MINUTE: int = 1
BASE_HAPPINESS: int = 100
BASE_MULTIPLIER_MIN: float = 0.6
BASE_MULTIPLIER_MAX: float = 1.2


def income_multiplier(happiness: int) -> float:
    """Вычисляет мультипликатор доходов на основе счастья."""

    happiness = max(0, min(200, happiness))
    return BASE_MULTIPLIER_MIN + (BASE_MULTIPLIER_MAX - BASE_MULTIPLIER_MIN) * (happiness / 200)
