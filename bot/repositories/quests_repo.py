"""Репозиторий квестов."""
from __future__ import annotations

import json
from typing import Dict, List


class QuestsRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def templates_by_kind(self, kind: str) -> List[Dict[str, str]]:
        rows = await self.db.fetchall("SELECT payload_json FROM quests WHERE kind=?", kind)
        return [json.loads(row[0]) for row in rows]

    async def assign(self, user_id: int, quest_code: str) -> None:
        await self.db.execute(
            "INSERT OR IGNORE INTO user_quests(user_id, quest_code, progress) VALUES(?, ?, 0)",
            user_id,
            quest_code,
        )

    async def list_for_user(self, user_id: int) -> List[Dict[str, str | int]]:
        rows = await self.db.fetchall(
            "SELECT quest_code, progress, completed_at, claimed_at FROM user_quests WHERE user_id=?",
            user_id,
        )
        return [
            {
                "quest_code": row[0],
                "progress": row[1],
                "completed_at": row[2],
                "claimed_at": row[3],
            }
            for row in rows
        ]
