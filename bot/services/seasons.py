"""Сезонная прогрессия."""
from __future__ import annotations

from datetime import datetime, timezone

from repositories.seasons_repo import SeasonsRepository

EPOCH = datetime(2024, 1, 1, tzinfo=timezone.utc)


class SeasonsService:
    def __init__(self, repo: SeasonsRepository) -> None:
        self.repo = repo

    def current_index(self) -> int:
        delta = datetime.now(timezone.utc) - EPOCH
        return int(delta.total_seconds() // 604800)

    async def add_prestige(self, user_id: int, amount: int) -> None:
        await self.repo.add_prestige(user_id, self.current_index(), amount)
