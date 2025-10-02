"""Реферальная система."""
from __future__ import annotations

from typing import Dict

from repositories.referrals_repo import ReferralsRepository


class ReferralService:
    def __init__(self, repo: ReferralsRepository) -> None:
        self.repo = repo

    async def activate(self, user_id: int, code: str) -> bool:
        return await self.repo.activate(user_id, code)

    async def redeem(self, user_id: int, code: str) -> Dict | None:
        return await self.repo.redeem_promo(user_id, code)
