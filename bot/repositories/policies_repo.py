"""Репозиторий политик."""
from __future__ import annotations

from typing import Dict, List

from core.utils import now_utc


class PoliciesRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def active_policies(self, user_id: int) -> List[str]:
        rows = await self.db.fetchall("SELECT policy_code FROM policies WHERE user_id=? AND is_active=1", user_id)
        return [row[0] for row in rows]

    async def toggle(self, user_id: int, policy_code: str, active: bool) -> None:
        await self.db.execute(
            "INSERT INTO policies(user_id, policy_code, is_active, activated_at) VALUES(?, ?, ?, ?)"
            " ON CONFLICT(user_id, policy_code) DO UPDATE SET is_active=excluded.is_active, activated_at=excluded.activated_at",
            user_id,
            policy_code,
            1 if active else 0,
            now_utc().isoformat(),
        )
