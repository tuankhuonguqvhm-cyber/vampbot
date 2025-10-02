"""Репозиторий зданий."""
from __future__ import annotations

import json
from typing import Any, Dict, List


class BuildingsRepository:
    def __init__(self, db) -> None:
        self.db = db

    async def list_types(self, category: str | None = None) -> List[Dict[str, Any]]:
        if category:
            rows = await self.db.fetchall("SELECT * FROM building_types WHERE category=? ORDER BY name", category)
        else:
            rows = await self.db.fetchall("SELECT * FROM building_types ORDER BY name")
        return [self._row_to_dict(row) for row in rows]

    async def get(self, code: str) -> Dict[str, Any] | None:
        row = await self.db.fetchone("SELECT * FROM building_types WHERE code=?", code)
        return self._row_to_dict(row) if row else None

    def _row_to_dict(self, row: Any) -> Dict[str, Any]:
        return {
            "code": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "base_cost_money": row[4],
            "base_cost_mats": row[5],
            "base_energy": row[6],
            "base_income_money": row[7],
            "base_income_mats": row[8],
            "base_income_energy": row[9],
            "growth_cost": row[10],
            "growth_income": row[11],
            "requires": json.loads(row[12]),
            "modules": json.loads(row[13]),
            "levels": json.loads(row[14]),
        }
