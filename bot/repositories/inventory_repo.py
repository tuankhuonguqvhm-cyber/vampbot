"""Репозиторий для пользовательских зданий."""
from __future__ import annotations

import json
from datetime import timedelta
from typing import Any, Dict, List

from core.utils import now_utc


class InventoryRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def buildings_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        rows = await self.db.fetchall(
            "SELECT id, building_type_id, district_id, level, started_at, completes_at, is_active, modules_json FROM user_buildings WHERE user_id=?",
            user_id,
        )
        items = []
        for row in rows:
            items.append(
                {
                    "id": row[0],
                    "building_type_id": row[1],
                    "district_id": row[2],
                    "level": row[3],
                    "started_at": row[4],
                    "completes_at": row[5],
                    "is_active": bool(row[6]),
                    "modules": json.loads(row[7] or "[]"),
                }
            )
        return items

    async def create_building(self, user_id: int, building_type_id: str, district_id: int, level: int, minutes: int) -> int:
        async with self.db.transaction() as conn:
            started = now_utc()
            completes = started + timedelta(minutes=minutes)
            await conn.execute(
                "INSERT INTO user_buildings(user_id, building_type_id, district_id, level, started_at, completes_at, is_active) VALUES(?, ?, ?, ?, ?, ?, 0)",
                (
                    user_id,
                    building_type_id,
                    district_id,
                    level,
                    started.isoformat(),
                    completes.isoformat(),
                ),
            )
            cursor = await conn.execute("SELECT last_insert_rowid()")
            row = await cursor.fetchone()
            return row[0]
