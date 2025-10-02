"""Репозиторий аудита."""
from __future__ import annotations

from typing import List


class AuditRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def list_recent(self, limit: int = 20) -> List[tuple]:
        rows = await self.db.fetchall(
            "SELECT user_id, action, payload, created_at FROM audit_log ORDER BY id DESC LIMIT ?",
            limit,
        )
        return rows
