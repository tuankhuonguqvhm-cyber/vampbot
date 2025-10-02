"""Логика строительства."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from repositories.buildings_repo import BuildingsRepository
from repositories.inventory_repo import InventoryRepository
from repositories.users_repo import UsersRepository
from core.utils import now_utc


@dataclass
class BuildResult:
    ok: bool
    message: str


class BuildingService:
    def __init__(self, buildings: BuildingsRepository, inventory: InventoryRepository, users: UsersRepository) -> None:
        self.buildings = buildings
        self.inventory = inventory
        self.users = users

    async def start_build(self, user_id: int, building_code: str, district_id: int) -> BuildResult:
        building = await self.buildings.get(building_code)
        if not building:
            return BuildResult(False, "Неизвестное здание")
        user = await self.users.get_or_create(user_id, None, None)
        cost = building['base_cost_money']
        mats = building['base_cost_mats']
        if user['money'] < cost or user['mats'] < mats:
            return BuildResult(False, "Недостаточно ресурсов")
        await self.users.update_resources(
            user_id,
            user['money'] - cost,
            user['mats'] - mats,
            user['energy'],
            user['happiness'],
        )
        await self.inventory.create_building(user_id, building_code, district_id, 1, building['levels'][0]['time_minutes'])
        return BuildResult(True, "Стройка начата")
