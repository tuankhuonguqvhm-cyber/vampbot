"""Репозиторий рейтингов."""
from __future__ import annotations

from typing import Dict, List


class LeaderboardRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def top_prestige(self, limit: int = 10) -> List[Dict[str, str]]:
        rows = await self.db.fetchall(
            "SELECT u.username, s.prestige FROM user_season_scores s JOIN users u ON u.tg_id=s.user_id ORDER BY s.prestige DESC LIMIT ?",
            limit,
        )
        return [
            {"username": row[0] or "unknown", "score": row[1]} for row in rows
        ]
