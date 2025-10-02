"""Античит."""
from __future__ import annotations

from typing import Dict

from core.security import AnomalyDetector


class AntiCheatService:
    def __init__(self) -> None:
        self.detector = AnomalyDetector()

    def track_resources(self, user_id: int, delta: int) -> float:
        result = self.detector.observe(user_id, delta)
        return result.score
