"""CLI для управления базой."""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from config import CONFIG
from core.db import Database, check_integrity, vacuum


async def cmd_seed(db: Database) -> None:
    await db.seed_if_required()
    print("Сиды загружены")


async def cmd_backup(db: Database, dest: Path) -> None:
    data = await db.connection.iterdump()
    dest.write_text("\n".join(data), encoding="utf-8")
    print(f"Бэкап сохранён в {dest}")


async def cmd_restore(db: Database, src: Path) -> None:
    sql = src.read_text(encoding="utf-8")
    await db.connection.executescript(sql)
    print("База восстановлена")


async def cmd_vacuum(db: Database) -> None:
    await vacuum(db)
    print("VACUUM выполнен")


async def cmd_check(db: Database) -> None:
    result = await check_integrity(db)
    print("Integrity OK" if result else "Integrity FAILED")


async def cmd_simulate(db: Database) -> None:
    from scripts.simulate import run_simulation

    report = await run_simulation(db, users=50, ticks=100)
    print(json.dumps(report, ensure_ascii=False, indent=2))


async def main_async(args) -> None:
    db = Database(CONFIG.database_path)
    await db.setup()
    try:
        if args.command == "seed":
            await cmd_seed(db)
        elif args.command == "backup":
            await cmd_backup(db, Path(args.path))
        elif args.command == "restore":
            await cmd_restore(db, Path(args.path))
        elif args.command == "vacuum":
            await cmd_vacuum(db)
        elif args.command == "check-integrity":
            await cmd_check(db)
        elif args.command == "simulate":
            await cmd_simulate(db)
    finally:
        await db.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Утилита управления ботом")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed")
    p_backup = sub.add_parser("backup")
    p_backup.add_argument("path")
    p_restore = sub.add_parser("restore")
    p_restore.add_argument("path")
    sub.add_parser("vacuum")
    sub.add_parser("check-integrity")
    sub.add_parser("simulate")
    args = parser.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
