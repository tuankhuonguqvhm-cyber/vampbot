"""Простейший симулятор экономики."""
from __future__ import annotations

import asyncio
import random
from typing import Dict

from core.utils import now_utc
from repositories.users_repo import UsersRepository


async def run_simulation(db, users: int = 10, ticks: int = 100) -> Dict[str, float]:
    repo = UsersRepository(db)
    totals = {"money": 0, "mats": 0}
    for i in range(users):
        await repo.get_or_create(10_000 + i, f"user{i}", f"User {i}")
    for _ in range(ticks):
        user_id = 10_000 + random.randint(0, users - 1)
        user = await repo.get_or_create(user_id, f"user{user_id}", "Sim")
        delta_money = random.randint(10, 200)
        delta_mats = random.randint(0, 50)
        totals["money"] += delta_money
        totals["mats"] += delta_mats
        await repo.update_resources(
            user_id,
            user['money'] + delta_money,
            user['mats'] + delta_mats,
            min(user['energy'] + 1, 100),
            user['happiness'],
        )
        await asyncio.sleep(0)
    return {
        "users": users,
        "ticks": ticks,
        "money_generated": totals['money'],
        "mats_generated": totals['mats'],
        "timestamp": now_utc().isoformat(),
    }
