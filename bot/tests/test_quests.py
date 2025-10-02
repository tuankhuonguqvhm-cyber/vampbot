import unittest
from pathlib import Path

from core.db import Database
from repositories.quests_repo import QuestsRepository
from services.quests import QuestService


class QuestTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = Database(Path('test.db'))
        await self.db.setup()
        self.service = QuestService(QuestsRepository(self.db))

    async def asyncTearDown(self) -> None:
        await self.db.close()

    async def test_assign_daily(self):
        codes = await self.service.assign_daily(1)
        self.assertLessEqual(len(codes), 3)
