"""Работа с рейтингами."""
from __future__ import annotations

from typing import List

from repositories.leaderboard_repo import LeaderboardRepository


class LeaderboardService:
    def __init__(self, repo: LeaderboardRepository) -> None:
        self.repo = repo

    async def top_prestige(self, limit: int = 10) -> List[dict]:
        return await self.repo.top_prestige(limit)
