"""Сервис рынка."""
from __future__ import annotations

from typing import Dict, List

from core.utils import z_score
from repositories.market_repo import MarketRepository


class MarketService:
    def __init__(self, repo: MarketRepository) -> None:
        self.repo = repo
        self.history: Dict[str, List[int]] = {}

    async def create_order(self, user_id: int, kind: str, resource: str, qty: int, price: int) -> int:
        order_id = await self.repo.create_order(user_id, kind, resource, qty, price)
        self.history.setdefault(resource, []).append(price)
        return order_id

    async def recommended_price(self, resource: str, base: float) -> float:
        series = self.history.get(resource, [base])
        return base * (1 + 0.05 * z_score(series))
