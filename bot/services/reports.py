"""Генерация отчётов."""
from __future__ import annotations

from typing import List

from repositories.audit_repo import AuditRepository


class ReportService:
    def __init__(self, repo: AuditRepository) -> None:
        self.repo = repo

    async def recent(self) -> List[str]:
        rows = await self.repo.list_recent()
        return [f"[{row[3]}] {row[1]}: {row[2]}" for row in rows]
