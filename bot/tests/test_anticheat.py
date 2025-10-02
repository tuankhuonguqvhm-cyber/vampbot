import unittest

from services.anticheat import AntiCheatService


class AntiCheatTest(unittest.TestCase):
    def test_track(self):
        service = AntiCheatService()
        score = service.track_resources(1, 100)
        self.assertIsInstance(score, float)
