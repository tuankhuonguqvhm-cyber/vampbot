"""Логика достижений."""
from __future__ import annotations

from typing import Dict

from repositories.achievements_repo import AchievementsRepository


class AchievementService:
    def __init__(self, repo: AchievementsRepository) -> None:
        self.repo = repo

    async def progress(self, user_id: int) -> Dict[str, Dict[str, int | str]]:
        return await self.repo.progress_for_user(user_id)

    async def update(self, user_id: int, ach_code: str, value: int) -> None:
        await self.repo.update_progress(user_id, ach_code, value)
