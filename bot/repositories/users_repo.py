"""Репозиторий пользователей."""
from __future__ import annotations

from typing import Any, Dict, Optional

from core.utils import now_utc


class UsersRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def get_or_create(self, tg_id: int, username: str | None, first_name: str | None) -> Dict[str, Any]:
        row = await self.db.fetchone("SELECT * FROM users WHERE tg_id=?", tg_id)
        if row:
            return self._row_to_dict(row)
        now = now_utc().isoformat()
        await self.db.execute(
            "INSERT INTO users(tg_id, username, first_name, money, mats, energy, happiness, pop, infra_lvl, last_tick_at, created_at) "
            "VALUES(?, ?, ?, 500, 200, 100, 120, 1000, 1, ?, ?)",
            tg_id,
            username,
            first_name,
            now,
            now,
        )
        row = await self.db.fetchone("SELECT * FROM users WHERE tg_id=?", tg_id)
        return self._row_to_dict(row)

    async def update_resources(self, tg_id: int, money: int, mats: int, energy: int, happiness: int) -> None:
        await self.db.execute(
            "UPDATE users SET money=?, mats=?, energy=?, happiness=? WHERE tg_id=?",
            money,
            mats,
            energy,
            happiness,
            tg_id,
        )

    async def set_city(self, tg_id: int, city_id: int) -> None:
        await self.db.execute("UPDATE users SET city_id=? WHERE tg_id=?", city_id, tg_id)

    async def update_tick(self, tg_id: int, money: int, mats: int, energy: int, happiness: int, pop: int, infra_lvl: int) -> None:
        await self.db.execute(
            "UPDATE users SET money=?, mats=?, energy=?, happiness=?, pop=?, infra_lvl=?, last_tick_at=? WHERE tg_id=?",
            money,
            mats,
            energy,
            happiness,
            pop,
            infra_lvl,
            now_utc().isoformat(),
            tg_id,
        )

    def _row_to_dict(self, row: Any) -> Dict[str, Any]:
        columns = [
            "tg_id", "username", "first_name", "city_id", "money", "mats", "energy", "happiness",
            "pop", "infra_lvl", "last_tick_at", "created_at", "treasury"
        ]
        return {col: row[idx] for idx, col in enumerate(columns)}
