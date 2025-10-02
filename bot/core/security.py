"""Сервисы безопасности и античита."""
from __future__ import annotations

import logging
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Deque, Dict, Tuple

from core.utils import now_utc, z_score

LOGGER = logging.getLogger(__name__)


class IdempotencyService:
    """Регистрирует nonce в БД, предотвращая повтор."""

    def __init__(self, db) -> None:
        self.db = db

    async def register_nonce(self, nonce: str) -> bool:
        query = "INSERT OR IGNORE INTO idempotency(key, created_at) VALUES(?, ?)"
        now = now_utc().isoformat()
        await self.db.connection.execute(query, (nonce, now))
        await self.db.connection.commit()
        cursor = await self.db.connection.execute("SELECT changes()")
        inserted = (await cursor.fetchone())[0]
        return inserted > 0


class RateLimiter:
    """Rate limit с хранением в памяти и БД."""

    def __init__(self, db, cooldown: timedelta) -> None:
        self.db = db
        self.cooldown = cooldown
        self.memory: Dict[Tuple[int, str], datetime] = {}

    async def check(self, user_id: int, action: str) -> bool:
        now = now_utc()
        key = (user_id, action)
        last = self.memory.get(key)
        if last and now - last < self.cooldown:
            return False
        row = await self.db.fetchone(
            "SELECT ts FROM rate_limit WHERE user_id=? AND action=? ORDER BY ts DESC LIMIT 1",
            user_id,
            action,
        )
        if row:
            ts = datetime.fromisoformat(row[0])
            if now - ts < self.cooldown:
                return False
        await self.db.execute(
            "INSERT INTO rate_limit(user_id, action, ts) VALUES(?, ?, ?)",
            user_id,
            action,
            now.isoformat(),
        )
        self.memory[key] = now
        return True


@dataclass
class AnomalyResult:
    score: float
    reason: str


class AnomalyDetector:
    """Простая эвристика для античита."""

    def __init__(self) -> None:
        self.history: Dict[int, Deque[int]] = defaultdict(lambda: deque(maxlen=20))

    def observe(self, user_id: int, delta: int) -> AnomalyResult:
        history = self.history[user_id]
        history.append(delta)
        if len(history) < 5:
            return AnomalyResult(score=0.0, reason="Недостаточно данных")
        score = z_score(list(history))
        if score > 3:
            reason = "Аномальный рост ресурсов"
            LOGGER.warning("User %s flagged: z-score %.2f", user_id, score)
            return AnomalyResult(score=score, reason=reason)
        return AnomalyResult(score=score, reason="OK")


async def audit(db, user_id: int, action: str, payload: str) -> None:
    """Записывает действие в журнал."""

    await db.execute(
        "INSERT INTO audit_log(user_id, action, payload, created_at) VALUES(?, ?, ?, ?)",
        user_id,
        action,
        payload,
        now_utc().isoformat(),
    )
