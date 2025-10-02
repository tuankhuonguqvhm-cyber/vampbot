"""Репозиторий сезонов."""
from __future__ import annotations

from typing import Optional


class SeasonsRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def get_prestige(self, user_id: int, season_index: int) -> int:
        row = await self.db.fetchone(
            "SELECT prestige FROM user_season_scores WHERE user_id=? AND season_index=?",
            user_id,
            season_index,
        )
        return row[0] if row else 0

    async def add_prestige(self, user_id: int, season_index: int, amount: int) -> None:
        await self.db.execute(
            "INSERT INTO user_season_scores(user_id, season_index, prestige) VALUES(?, ?, ?)"
            " ON CONFLICT(user_id, season_index) DO UPDATE SET prestige=prestige+excluded.prestige",
            user_id,
            season_index,
            amount,
        )
