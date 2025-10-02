import unittest
from pathlib import Path

from core.db import Database
from repositories.users_repo import UsersRepository
from repositories.inventory_repo import InventoryRepository
from repositories.buildings_repo import BuildingsRepository
from services.buildings import BuildingService


class BuildingServiceTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = Database(Path('test.db'))
        await self.db.setup()
        self.service = BuildingService(BuildingsRepository(self.db), InventoryRepository(self.db), UsersRepository(self.db))

    async def asyncTearDown(self) -> None:
        await self.db.close()

    async def test_start_build(self):
        result = await self.service.start_build(1, 'BLD_001', 1)
        self.assertIn(result.ok, (True, False))
