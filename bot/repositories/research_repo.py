"""Репозиторий исследований."""
from __future__ import annotations

from typing import Dict, List


class ResearchRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def list_for_user(self, user_id: int) -> List[Dict[str, int]]:
        rows = await self.db.fetchall("SELECT tech_code, level FROM research WHERE user_id=?", user_id)
        return [{"tech_code": row[0], "level": row[1]} for row in rows]

    async def set_level(self, user_id: int, tech_code: str, level: int) -> None:
        await self.db.execute(
            "INSERT INTO research(user_id, tech_code, level) VALUES(?, ?, ?) ON CONFLICT(user_id, tech_code) DO UPDATE SET level=excluded.level",
            user_id,
            tech_code,
            level,
        )
