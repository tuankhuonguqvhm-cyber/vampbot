"""Сервис офлайн-тиков экономики."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Tuple

from core.models import MAX_ENERGY, ENERGY_REGEN_PER_MINUTE, income_multiplier
from core.utils import now_utc
from repositories.users_repo import UsersRepository
from repositories.buildings_repo import BuildingsRepository
from repositories.inventory_repo import InventoryRepository
from repositories.policies_repo import PoliciesRepository
from repositories.research_repo import ResearchRepository


@dataclass
class TickResult:
    money_delta: int
    mats_delta: int
    energy_delta: int
    minutes: int


class TickService:
    """Пересчитывает офлайн-прогресс пользователя."""

    def __init__(
        self,
        users: UsersRepository,
        buildings: InventoryRepository,
        building_types: BuildingsRepository,
        policies: PoliciesRepository,
        research: ResearchRepository,
    ) -> None:
        self.users = users
        self.buildings = buildings
        self.building_types = building_types
        self.policies = policies
        self.research = research

    async def perform_tick(self, user_id: int) -> TickResult:
        user = await self.users.get_or_create(user_id, None, None)
        last_tick = user.get('last_tick_at')
        now = now_utc()
        if last_tick:
            last_dt = datetime.fromisoformat(last_tick)
        else:
            last_dt = now
        delta_minutes = max(0, int((now - last_dt).total_seconds() // 60))
        if delta_minutes == 0:
            delta_minutes = 1
        energy = min(MAX_ENERGY, user['energy'] + delta_minutes * ENERGY_REGEN_PER_MINUTE)
        active_buildings = await self.buildings.buildings_for_user(user_id)
        income_money = 0
        income_mats = 0
        income_energy = 0
        for entry in active_buildings:
            if not entry['is_active']:
                continue
            btype = await self.building_types.get(entry['building_type_id'])
            if not btype:
                continue
            level_info = btype['levels'][min(entry['level'] - 1, len(btype['levels']) - 1)]
            income_money += level_info['income_money']
            income_mats += level_info['income_mats']
            income_energy += level_info['income_energy']
        mult = income_multiplier(user['happiness'])
        money_gain = int(income_money * mult * delta_minutes)
        mats_gain = int(income_mats * mult * delta_minutes)
        energy = min(MAX_ENERGY, energy + int(income_energy * delta_minutes))
        await self.users.update_tick(
            user_id,
            user['money'] + money_gain,
            user['mats'] + mats_gain,
            energy,
            user['happiness'],
            user['pop'] + delta_minutes,
            user['infra_lvl'],
        )
        return TickResult(
            money_delta=money_gain,
            mats_delta=mats_gain,
            energy_delta=energy - user['energy'],
            minutes=delta_minutes,
        )
