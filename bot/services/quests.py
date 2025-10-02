"""Работа с квестами."""
from __future__ import annotations

import random
from typing import Dict, List

from repositories.quests_repo import QuestsRepository


class QuestService:
    def __init__(self, repo: QuestsRepository) -> None:
        self.repo = repo

    async def assign_daily(self, user_id: int) -> List[str]:
        templates = await self.repo.templates_by_kind('collect')
        choices = random.sample(templates, k=min(3, len(templates)))
        codes = []
        for item in choices:
            await self.repo.assign(user_id, item['code'])
            codes.append(item['code'])
        return codes

    async def list(self, user_id: int) -> List[Dict[str, str | int]]:
        return await self.repo.list_for_user(user_id)
