"""Работа с базой данных SQLite и загрузка сидов."""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List

import aiosqlite

from core.utils import now_utc

LOGGER = logging.getLogger(__name__)


SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS users (
        tg_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        city_id INTEGER,
        money INTEGER NOT NULL DEFAULT 0,
        mats INTEGER NOT NULL DEFAULT 0,
        energy INTEGER NOT NULL DEFAULT 100,
        happiness INTEGER NOT NULL DEFAULT 100,
        pop INTEGER NOT NULL DEFAULT 0,
        infra_lvl INTEGER NOT NULL DEFAULT 1,
        last_tick_at TEXT,
        created_at TEXT NOT NULL,
        treasury INTEGER NOT NULL DEFAULT 0
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country_code TEXT NOT NULL,
        emoji TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS building_types (
        code TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        base_cost_money INTEGER NOT NULL,
        base_cost_mats INTEGER NOT NULL,
        base_energy INTEGER NOT NULL,
        base_income_money INTEGER NOT NULL,
        base_income_mats INTEGER NOT NULL,
        base_income_energy INTEGER NOT NULL,
        growth_cost REAL NOT NULL,
        growth_income REAL NOT NULL,
        requires_json TEXT NOT NULL,
        modules_json TEXT NOT NULL,
        levels_json TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_buildings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        building_type_id TEXT NOT NULL,
        district_id INTEGER NOT NULL,
        level INTEGER NOT NULL,
        started_at TEXT,
        completes_at TEXT,
        is_active INTEGER NOT NULL DEFAULT 0,
        modules_json TEXT NOT NULL DEFAULT '[]',
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(building_type_id) REFERENCES building_types(code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS districts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        slot_limits_json TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS research (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        tech_code TEXT NOT NULL,
        level INTEGER NOT NULL,
        UNIQUE(user_id, tech_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS policies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        policy_code TEXT NOT NULL,
        is_active INTEGER NOT NULL DEFAULT 0,
        activated_at TEXT,
        UNIQUE(user_id, policy_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS landmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        lm_code TEXT NOT NULL,
        acquired_at TEXT NOT NULL,
        UNIQUE(user_id, lm_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        chat_id INTEGER NOT NULL,
        first_seen_at TEXT NOT NULL,
        UNIQUE(user_id, chat_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_season_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        season_index INTEGER NOT NULL,
        prestige INTEGER NOT NULL DEFAULT 0,
        UNIQUE(user_id, season_index)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS quests (
        code TEXT PRIMARY KEY,
        payload_json TEXT NOT NULL,
        kind TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        quest_code TEXT NOT NULL,
        progress INTEGER NOT NULL DEFAULT 0,
        completed_at TEXT,
        claimed_at TEXT,
        UNIQUE(user_id, quest_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(quest_code) REFERENCES quests(code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS achievements (
        code TEXT PRIMARY KEY,
        payload_json TEXT NOT NULL,
        category TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ach_code TEXT NOT NULL,
        progress INTEGER NOT NULL DEFAULT 0,
        unlocked_at TEXT,
        UNIQUE(user_id, ach_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(ach_code) REFERENCES achievements(code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS titles (
        code TEXT PRIMARY KEY,
        payload_json TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_titles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title_code TEXT NOT NULL,
        equipped INTEGER NOT NULL DEFAULT 0,
        UNIQUE(user_id, title_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(title_code) REFERENCES titles(code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS events_active (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        event_code TEXT NOT NULL,
        started_at TEXT NOT NULL,
        ends_at TEXT NOT NULL,
        payload_json TEXT NOT NULL,
        UNIQUE(user_id, event_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS market_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        kind TEXT NOT NULL,
        resource TEXT NOT NULL,
        qty INTEGER NOT NULL,
        price INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        status TEXT NOT NULL,
        matched_qty INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        buyer_id INTEGER NOT NULL,
        seller_id INTEGER NOT NULL,
        qty INTEGER NOT NULL,
        price INTEGER NOT NULL,
        executed_at TEXT NOT NULL,
        FOREIGN KEY(order_id) REFERENCES market_orders(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS clans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tag TEXT NOT NULL,
        created_at TEXT NOT NULL,
        leader_user_id INTEGER NOT NULL,
        UNIQUE(tag),
        FOREIGN KEY(leader_user_id) REFERENCES users(tg_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS clan_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clan_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        joined_at TEXT NOT NULL,
        UNIQUE(clan_id, user_id),
        FOREIGN KEY(clan_id) REFERENCES clans(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS clan_projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clan_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        progress INTEGER NOT NULL DEFAULT 0,
        target INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        completed_at TEXT,
        UNIQUE(clan_id, code),
        FOREIGN KEY(clan_id) REFERENCES clans(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS clan_votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clan_id INTEGER NOT NULL,
        topic TEXT NOT NULL,
        created_at TEXT NOT NULL,
        ends_at TEXT NOT NULL,
        yes INTEGER NOT NULL DEFAULT 0,
        no INTEGER NOT NULL DEFAULT 0,
        abstain INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(clan_id) REFERENCES clans(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS clan_votes_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vote_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        choice TEXT NOT NULL,
        UNIQUE(vote_id, user_id),
        FOREIGN KEY(vote_id) REFERENCES clan_votes(id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS duels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        a_user_id INTEGER NOT NULL,
        b_user_id INTEGER NOT NULL,
        rules_json TEXT NOT NULL,
        started_at TEXT NOT NULL,
        ends_at TEXT,
        result_json TEXT,
        FOREIGN KEY(a_user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(b_user_id) REFERENCES users(tg_id) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS referrals (
        ref_code TEXT PRIMARY KEY,
        inviter_user_id INTEGER,
        uses_left INTEGER NOT NULL,
        expires_at TEXT,
        FOREIGN KEY(inviter_user_id) REFERENCES users(tg_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_referrals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        ref_code TEXT NOT NULL,
        activated_at TEXT NOT NULL,
        UNIQUE(user_id, ref_code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(ref_code) REFERENCES referrals(ref_code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS promo_codes (
        code TEXT PRIMARY KEY,
        reward_json TEXT NOT NULL,
        uses_left INTEGER NOT NULL,
        expires_at TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS user_promos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        code TEXT NOT NULL,
        redeemed_at TEXT NOT NULL,
        UNIQUE(user_id, code),
        FOREIGN KEY(user_id) REFERENCES users(tg_id) ON DELETE CASCADE,
        FOREIGN KEY(code) REFERENCES promo_codes(code) ON DELETE CASCADE
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        payload TEXT,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS idempotency (
        key TEXT PRIMARY KEY,
        created_at TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS rate_limit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action TEXT NOT NULL,
        ts TEXT NOT NULL
    );
    """
]


INDICES = [
    "CREATE INDEX IF NOT EXISTS idx_user_season ON user_season_scores(user_id, season_index);",
    "CREATE INDEX IF NOT EXISTS idx_market_active ON market_orders(status, resource);",
    "CREATE INDEX IF NOT EXISTS idx_clan_members ON clan_members(clan_id);",
    "CREATE INDEX IF NOT EXISTS idx_user_buildings ON user_buildings(user_id, is_active);",
    "CREATE INDEX IF NOT EXISTS idx_user_chats_chat ON user_chats(chat_id);",
]


class Database:
    """Инкапсулирует доступ к SQLite базе."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._conn: aiosqlite.Connection | None = None
        self._lock = asyncio.Lock()

    async def setup(self) -> None:
        """Открывает соединение, применяет PRAGMA и миграции."""

        LOGGER.info("Подготовка базы данных %s", self.path)
        self._conn = await aiosqlite.connect(self.path)
        await self._conn.execute("PRAGMA foreign_keys=ON;")
        await self._conn.execute("PRAGMA journal_mode=WAL;")
        await self._conn.execute("PRAGMA synchronous=NORMAL;")
        await self._conn.execute("PRAGMA temp_store=MEMORY;")
        await self._conn.commit()
        await self.apply_schema()
        await self.seed_if_required()

    async def close(self) -> None:
        if self._conn:
            await self._conn.close()
            self._conn = None

    @property
    def connection(self) -> aiosqlite.Connection:
        if not self._conn:
            raise RuntimeError("База данных не инициализирована")
        return self._conn

    async def apply_schema(self) -> None:
        """Применяет схемы таблиц и индексы."""

        assert self._conn
        for statement in SCHEMA:
            await self._conn.execute(statement)
        for statement in INDICES:
            await self._conn.execute(statement)
        await self._conn.commit()

    async def seed_if_required(self) -> None:
        """Загружает сиды из директории data."""

        assert self._conn
        cursor = await self._conn.execute("SELECT COUNT(*) FROM cities")
        count_cities = (await cursor.fetchone())[0]
        if count_cities == 0:
            LOGGER.info("Импортируем сиды городов")
            await self._seed_json_table("data/cities_ru.json", "cities", self._insert_cities)
        cursor = await self._conn.execute("SELECT COUNT(*) FROM building_types")
        if (await cursor.fetchone())[0] == 0:
            LOGGER.info("Импортируем сиды зданий")
            await self._seed_json_table("data/buildings.json", "building_types", self._insert_buildings)
        cursor = await self._conn.execute("SELECT COUNT(*) FROM quests")
        if (await cursor.fetchone())[0] == 0:
            LOGGER.info("Импортируем сиды квестов")
            await self._seed_json_table("data/quests_daily.json", "quests", self._insert_quests)
            await self._seed_json_table("data/quests_weekly.json", "quests", self._insert_quests)
        cursor = await self._conn.execute("SELECT COUNT(*) FROM achievements")
        if (await cursor.fetchone())[0] == 0:
            LOGGER.info("Импортируем сиды достижений")
            await self._seed_json_table("data/achievements.json", "achievements", self._insert_achievements)
        cursor = await self._conn.execute("SELECT COUNT(*) FROM titles")
        if (await cursor.fetchone())[0] == 0:
            await self._seed_json_table("data/titles.json", "titles", self._insert_titles)
        cursor = await self._conn.execute("SELECT COUNT(*) FROM promo_codes")
        if (await cursor.fetchone())[0] == 0:
            await self._seed_json_table("data/promo_codes.json", "promo_codes", self._insert_promos)

    async def _seed_json_table(
        self, relative: str, name: str, inserter: Any
    ) -> None:
        """Читает JSON и вызывает конкретный вставщик."""

        path = Path(__file__).resolve().parent.parent / relative
        data_raw = path.read_text(encoding="utf-8")
        payload = json.loads(data_raw)
        await inserter(payload)
        await self._conn.commit()
        LOGGER.info("Импорт %s завершён (%s записей)", name, len(payload))

    async def _insert_cities(self, cities: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        await self._conn.executemany(
            "INSERT INTO cities(id, name, country_code, emoji) VALUES(:id, :name, :country_code, :emoji)",
            cities,
        )

    async def _insert_buildings(self, buildings: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        rows = [
            {
                "code": item["code"],
                "name": item["name"],
                "category": item["category"],
                "description": item["description"],
                "base_cost_money": item["base_cost_money"],
                "base_cost_mats": item["base_cost_mats"],
                "base_energy": item["base_energy"],
                "base_income_money": item["base_income_money"],
                "base_income_mats": item["base_income_mats"],
                "base_income_energy": item["base_income_energy"],
                "growth_cost": item["growth_cost"],
                "growth_income": item["growth_income"],
                "requires_json": json.dumps(item.get("requires", {}), ensure_ascii=False),
                "modules_json": json.dumps(item.get("modules", []), ensure_ascii=False),
                "levels_json": json.dumps(item.get("levels", []), ensure_ascii=False),
            }
            for item in buildings
        ]
        await self._conn.executemany(
            """
            INSERT INTO building_types(
                code, name, category, description, base_cost_money, base_cost_mats,
                base_energy, base_income_money, base_income_mats, base_income_energy,
                growth_cost, growth_income, requires_json, modules_json, levels_json
            ) VALUES(
                :code, :name, :category, :description, :base_cost_money, :base_cost_mats,
                :base_energy, :base_income_money, :base_income_mats, :base_income_energy,
                :growth_cost, :growth_income, :requires_json, :modules_json, :levels_json
            )
            """,
            rows,
        )

    async def _insert_quests(self, quests: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        rows = [
            {
                "code": item["code"],
                "payload_json": json.dumps(item, ensure_ascii=False),
                "kind": item.get("kind", "misc"),
            }
            for item in quests
        ]
        await self._conn.executemany(
            "INSERT INTO quests(code, payload_json, kind) VALUES(:code, :payload_json, :kind)",
            rows,
        )

    async def _insert_achievements(self, items: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        rows = [
            {
                "code": item["code"],
                "payload_json": json.dumps(item, ensure_ascii=False),
                "category": item.get("category", "general"),
            }
            for item in items
        ]
        await self._conn.executemany(
            "INSERT INTO achievements(code, payload_json, category) VALUES(:code, :payload_json, :category)",
            rows,
        )

    async def _insert_titles(self, items: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        rows = [
            {
                "code": item["code"],
                "payload_json": json.dumps(item, ensure_ascii=False),
            }
            for item in items
        ]
        await self._conn.executemany(
            "INSERT INTO titles(code, payload_json) VALUES(:code, :payload_json)",
            rows,
        )

    async def _insert_promos(self, items: Iterable[Dict[str, Any]]) -> None:
        assert self._conn
        rows = []
        now = now_utc()
        for item in items:
            expires_at = None
            days = item.get("expires_in_days")
            if days is not None:
                expires_at = (now + timedelta(days=days)).isoformat()
            rows.append(
                {
                    "code": item["code"],
                    "reward_json": json.dumps(item["reward"], ensure_ascii=False),
                    "uses_left": item.get("uses_left", 0),
                    "expires_at": expires_at,
                }
            )
        await self._conn.executemany(
            "INSERT INTO promo_codes(code, reward_json, uses_left, expires_at) VALUES(:code, :reward_json, :uses_left, :expires_at)",
            rows,
        )

    async def execute(self, sql: str, *args: Any) -> None:
        """Выполняет запрос без возврата результата."""

        async with self.connection.execute(sql, args) as cursor:
            await cursor.close()
        await self.connection.commit()

    async def fetchone(self, sql: str, *args: Any) -> Any:
        async with self.connection.execute(sql, args) as cursor:
            return await cursor.fetchone()

    async def fetchall(self, sql: str, *args: Any) -> List[Any]:
        async with self.connection.execute(sql, args) as cursor:
            return await cursor.fetchall()

    async def transaction(self):
        """Контекстный менеджер транзакции."""

        class _Txn:
            def __init__(self, db: "Database") -> None:
                self.db = db

            async def __aenter__(self) -> aiosqlite.Connection:
                await self.db.connection.execute("BEGIN")
                return self.db.connection

            async def __aexit__(self, exc_type, exc, tb) -> None:
                if exc:
                    await self.db.connection.execute("ROLLBACK")
                else:
                    await self.db.connection.execute("COMMIT")

        return _Txn(self)


async def vacuum(db: Database) -> None:
    """Выполняет VACUUM."""

    await db.connection.execute("VACUUM")
    await db.connection.commit()


async def check_integrity(db: Database) -> bool:
    """Проверяет целостность базы."""

    async with db.connection.execute("PRAGMA integrity_check;") as cursor:
        row = await cursor.fetchone()
        return row[0] == "ok"
