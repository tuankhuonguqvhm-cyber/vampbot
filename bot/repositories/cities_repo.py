"""Репозиторий городов."""
from __future__ import annotations

from typing import Any, Dict, List


class CitiesRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def all(self) -> List[Dict[str, Any]]:
        rows = await self.db.fetchall("SELECT id, name, country_code, emoji FROM cities ORDER BY name")
        return [
            {"id": row[0], "name": row[1], "country_code": row[2], "emoji": row[3]} for row in rows
        ]

    async def get(self, city_id: int) -> Dict[str, Any] | None:
        row = await self.db.fetchone("SELECT id, name, country_code, emoji FROM cities WHERE id=?", city_id)
        if not row:
            return None
        return {"id": row[0], "name": row[1], "country_code": row[2], "emoji": row[3]}
