import unittest
from pathlib import Path

from core.db import Database
from repositories.market_repo import MarketRepository
from services.market import MarketService


class MarketTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = Database(Path('test.db'))
        await self.db.setup()
        self.service = MarketService(MarketRepository(self.db))

    async def asyncTearDown(self) -> None:
        await self.db.close()

    async def test_create_order(self):
        order_id = await self.service.create_order(1, 'sell', 'mats', 5, 100)
        self.assertIsInstance(order_id, int)
