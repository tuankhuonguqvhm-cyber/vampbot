"""Асинхронные дуэли."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from core.utils import rand_nonce


@dataclass
class Duel:
    id: str
    opponent_id: int
    wager: int
    result: str | None = None


class DuelService:
    def __init__(self) -> None:
        self.active: Dict[int, Duel] = {}

    def create(self, user_id: int, opponent_id: int, wager: int) -> Duel:
        duel = Duel(id=rand_nonce(), opponent_id=opponent_id, wager=wager)
        self.active[user_id] = duel
        return duel

    def resolve(self, user_id: int, won: bool) -> Duel | None:
        duel = self.active.pop(user_id, None)
        if duel:
            duel.result = 'win' if won else 'lose'
        return duel
