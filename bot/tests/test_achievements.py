import unittest
from pathlib import Path

from core.db import Database
from repositories.achievements_repo import AchievementsRepository
from services.achievements import AchievementService


class AchievementTest(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.db = Database(Path('test.db'))
        await self.db.setup()
        self.service = AchievementService(AchievementsRepository(self.db))

    async def asyncTearDown(self) -> None:
        await self.db.close()

    async def test_progress(self):
        progress = await self.service.progress(1)
        self.assertIsInstance(progress, dict)
