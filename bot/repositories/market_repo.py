"""Репозиторий рынка."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from core.utils import now_utc


class MarketRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def create_order(self, user_id: int, kind: str, resource: str, qty: int, price: int) -> int:
        async with self.db.transaction() as conn:
            await conn.execute(
                "INSERT INTO market_orders(user_id, kind, resource, qty, price, created_at, status) VALUES(?, ?, ?, ?, ?, ?, 'OPEN')",
                (user_id, kind, resource, qty, price, now_utc().isoformat()),
            )
            cursor = await conn.execute("SELECT last_insert_rowid()")
            return (await cursor.fetchone())[0]

    async def cancel_order(self, order_id: int) -> None:
        await self.db.execute("UPDATE market_orders SET status='CANCELLED' WHERE id=?", order_id)

    async def active_orders(self, resource: str) -> List[Dict[str, str | int]]:
        rows = await self.db.fetchall(
            "SELECT id, user_id, kind, qty, price, matched_qty FROM market_orders WHERE resource=? AND status='OPEN'",
            resource,
        )
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "kind": row[2],
                "qty": row[3],
                "price": row[4],
                "matched_qty": row[5],
            }
            for row in rows
        ]

    async def log_trade(self, order_id: int, buyer_id: int, seller_id: int, qty: int, price: int) -> None:
        await self.db.execute(
            "INSERT INTO trades(order_id, buyer_id, seller_id, qty, price, executed_at) VALUES(?, ?, ?, ?, ?, ?)",
            order_id,
            buyer_id,
            seller_id,
            qty,
            price,
            now_utc().isoformat(),
        )
