"""Управление политиками."""
from __future__ import annotations

from typing import List

from repositories.policies_repo import PoliciesRepository


class PoliciesService:
    def __init__(self, repo: PoliciesRepository) -> None:
        self.repo = repo

    async def toggle(self, user_id: int, policy_code: str, active: bool) -> None:
        await self.repo.toggle(user_id, policy_code, active)

    async def active(self, user_id: int) -> List[str]:
        return await self.repo.active_policies(user_id)
