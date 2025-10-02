"""Репозиторий кланов."""
from __future__ import annotations

from typing import Dict, List

from core.utils import now_utc


class ClansRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def create(self, leader_id: int, name: str, tag: str) -> int:
        async with self.db.transaction() as conn:
            await conn.execute(
                "INSERT INTO clans(name, tag, created_at, leader_user_id) VALUES(?, ?, ?, ?)",
                (name, tag, now_utc().isoformat(), leader_id),
            )
            cursor = await conn.execute("SELECT last_insert_rowid()")
            clan_id = (await cursor.fetchone())[0]
            await conn.execute(
                "INSERT INTO clan_members(clan_id, user_id, role, joined_at) VALUES(?, ?, 'leader', ?)",
                (clan_id, leader_id, now_utc().isoformat()),
            )
            return clan_id

    async def members(self, clan_id: int) -> List[Dict[str, str]]:
        rows = await self.db.fetchall(
            "SELECT user_id, role, joined_at FROM clan_members WHERE clan_id=?",
            clan_id,
        )
        return [
            {"user_id": row[0], "role": row[1], "joined_at": row[2]} for row in rows
        ]
