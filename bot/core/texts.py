"""Шаблоны текстов бота."""
from __future__ import annotations

from typing import Dict

from core.utils import fmt_number


def city_summary(user: Dict[str, int], city: Dict[str, str], season: int, incomes: Dict[str, int]) -> str:
    """Формирует сводку города."""

    mult = user.get("mult", 1.0)
    return (
        f"🏙️ {city['emoji']} {city['name']} | Сезон #{season}\n"
        f"Ресурсы: 💰{fmt_number(user['money'])} 🧱{fmt_number(user['mats'])} ⚡{user['energy']}/100  😊{user['happiness']} (x{mult:.2f})\n"
        f"Население: {fmt_number(user['pop'])} | Инфра: {user['infra_lvl']}\n"
        f"Доход/мин: 💰{fmt_number(incomes['money'])} 🧱{fmt_number(incomes['mats'])} ⚡{fmt_number(incomes['energy'])}\n"
    )


def format_leaderboard(title: str, page: int, pages: int, rows: Dict[int, Dict[str, str]]) -> str:
    lines = [title]
    for idx, row in rows.items():
        lines.append(f"{idx}) @{row['username']} — {fmt_number(row['score'])} ⭐")
    lines.append(f"стр. {page}/{pages}")
    return "\n".join(lines)


ERROR_RATE_LIMIT = "Слишком часто, попробуйте чуть позже."
ERROR_NOT_ENOUGH = "Недостаточно ресурсов для действия."
ERROR_UNEXPECTED = "Произошла ошибка. Повторите попытку позже."


HELP_TEXT = (
    "<b>Городской Рывок+</b> — текстовый симулятор города.\n"
    "Доступные команды:\n"
    "/menu — открыть главное меню\n"
    "/city — сводка города\n"
    "/build — мастер строительства\n"
    "/research — исследования\n"
    "/policies — управление политиками\n"
    "/market — рынок и P2P торговля\n"
    "/clan — управление кланом\n"
    "/duel — дуэли\n"
    "/quests — квесты и сезонные задачи\n"
    "/achievements — просмотр достижений\n"
    "Используйте кнопки меню для быстрого доступа к функциям."
)
