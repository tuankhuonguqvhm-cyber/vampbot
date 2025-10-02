"""Формулы счастья."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HappinessContext:
    base: int
    building_bonus: int
    event_bonus: int
    policy_bonus: int


def calculate_happiness(ctx: HappinessContext) -> int:
    value = ctx.base + ctx.building_bonus + ctx.event_bonus + ctx.policy_bonus
    return max(0, min(200, value))
