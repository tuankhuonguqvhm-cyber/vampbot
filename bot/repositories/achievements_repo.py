"""Репозиторий достижений."""
from __future__ import annotations

import json
from typing import Dict, List


class AchievementsRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def list_templates(self) -> List[Dict[str, str]]:
        rows = await self.db.fetchall("SELECT code, payload_json FROM achievements")
        return [json.loads(row[1]) for row in rows]

    async def progress_for_user(self, user_id: int) -> Dict[str, Dict[str, int | str]]:
        rows = await self.db.fetchall("SELECT ach_code, progress, unlocked_at FROM user_achievements WHERE user_id=?", user_id)
        return {
            row[0]: {"progress": row[1], "unlocked_at": row[2]} for row in rows
        }

    async def update_progress(self, user_id: int, ach_code: str, progress: int) -> None:
        await self.db.execute(
            "INSERT INTO user_achievements(user_id, ach_code, progress, unlocked_at) VALUES(?, ?, ?, NULL)"
            " ON CONFLICT(user_id, ach_code) DO UPDATE SET progress=excluded.progress",
            user_id,
            ach_code,
            progress,
        )
