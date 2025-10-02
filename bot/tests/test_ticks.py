import asyncio
import unittest
from datetime import datetime, timezone
from pathlib import Path

from core.db import Database
from core.utils import now_utc
from repositories.users_repo import UsersRepository
from repositories.inventory_repo import InventoryRepository
from repositories.buildings_repo import BuildingsRepository
from repositories.policies_repo import PoliciesRepository
from repositories.research_repo import ResearchRepository
from services.ticks import TickService


class TickTestCase(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = Database(Path('test.db'))
        await self.db.setup()
        self.users = UsersRepository(self.db)
        self.inventory = InventoryRepository(self.db)
        self.buildings = BuildingsRepository(self.db)
        self.policies = PoliciesRepository(self.db)
        self.research = ResearchRepository(self.db)
        self.service = TickService(self.users, self.inventory, self.buildings, self.policies, self.research)

    async def asyncTearDown(self) -> None:
        await self.db.close()

    async def test_tick_produces_gain(self):
        user = await self.users.get_or_create(1, 'tester', 'Tester')
        result = await self.service.perform_tick(user['tg_id'])
        self.assertGreaterEqual(result.minutes, 1)


if __name__ == '__main__':
    unittest.main()
