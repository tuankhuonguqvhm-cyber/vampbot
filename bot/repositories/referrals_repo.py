"""Репозиторий рефералов и промокодов."""
from __future__ import annotations

from datetime import datetime


class ReferralsRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def activate(self, user_id: int, ref_code: str) -> bool:
        row = await self.db.fetchone("SELECT uses_left, expires_at FROM referrals WHERE ref_code=?", ref_code)
        if not row:
            return False
        uses_left, expires_at = row
        if uses_left <= 0:
            return False
        if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
            return False
        await self.db.execute(
            "UPDATE referrals SET uses_left=uses_left-1 WHERE ref_code=?",
            ref_code,
        )
        await self.db.execute(
            "INSERT INTO user_referrals(user_id, ref_code, activated_at) VALUES(?, ?, ?)",
            user_id,
            ref_code,
            datetime.utcnow().isoformat(),
        )
        return True

    async def redeem_promo(self, user_id: int, code: str) -> dict | None:
        row = await self.db.fetchone(
            "SELECT reward_json, uses_left, expires_at FROM promo_codes WHERE code=?",
            code,
        )
        if not row:
            return None
        reward_json, uses_left, expires_at = row
        if uses_left <= 0:
            return None
        if expires_at and datetime.fromisoformat(expires_at) < datetime.utcnow():
            return None
        await self.db.execute("UPDATE promo_codes SET uses_left=uses_left-1 WHERE code=?", code)
        await self.db.execute(
            "INSERT INTO user_promos(user_id, code, redeemed_at) VALUES(?, ?, ?)",
            user_id,
            code,
            datetime.utcnow().isoformat(),
        )
        import json
        return json.loads(reward_json)
