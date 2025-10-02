"""Обработка исследований."""
from __future__ import annotations

from typing import Dict

from repositories.research_repo import ResearchRepository


class ResearchService:
    def __init__(self, repo: ResearchRepository) -> None:
        self.repo = repo

    async def grant(self, user_id: int, tech_code: str, level: int = 1) -> None:
        await self.repo.set_level(user_id, tech_code, level)

    async def tree(self, user_id: int) -> Dict[str, int]:
        rows = await self.repo.list_for_user(user_id)
        return {row['tech_code']: row['level'] for row in rows}
