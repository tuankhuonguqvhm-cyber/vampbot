"""Утилиты для работы бота."""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
from datetime import datetime, timezone
from secrets import token_hex
from typing import Any, Dict, Iterable, List, Sequence


def now_utc() -> datetime:
    """Возвращает текущее время в UTC."""

    return datetime.now(timezone.utc)


def fmt_number(value: int) -> str:
    """Форматирует число с разделителями."""

    return f"{value:,}".replace(",", "\u202f")


def humanize_timedelta(minutes: int) -> str:
    """Преобразует минуты в человекочитаемый формат."""

    hours, mins = divmod(minutes, 60)
    if hours and mins:
        return f"{hours} ч {mins} мин"
    if hours:
        return f"{hours} ч"
    return f"{mins} мин"


def rand_weighted(weights: Dict[str, float]) -> str:
    """Выбирает ключ по весам."""

    total = sum(weights.values())
    if total <= 0:
        raise ValueError("Сумма весов должна быть положительной")
    r = random.random() * total
    upto = 0.0
    for key, weight in weights.items():
        upto += weight
        if upto >= r:
            return key
    return next(iter(weights))


def rand_nonce() -> str:
    """Генерирует случайный nonce для callback."""

    return token_hex(8)


def clamp(value: float, min_value: float, max_value: float) -> float:
    """Ограничивает значение интервалом."""

    return max(min_value, min(max_value, value))


def hash_payload(payload: Dict[str, Any]) -> str:
    """Вычисляет хеш словаря."""

    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def paginator(items: Sequence[Any], page: int, per_page: int = 10) -> Dict[str, Any]:
    """Пагинация для списков."""

    total = len(items)
    pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, pages))
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "page": page,
        "pages": pages,
        "items": list(items[start:end]),
    }


def ensure_dir(path: str) -> None:
    """Создает директорию, если её нет."""

    os.makedirs(path, exist_ok=True)


def weighted_average(values: Iterable[float], weights: Iterable[float]) -> float:
    """Вычисляет среднее с весами."""

    values_list = list(values)
    weights_list = list(weights)
    if not values_list or not weights_list:
        return 0.0
    numerator = sum(v * w for v, w in zip(values_list, weights_list))
    denominator = sum(weights_list)
    if denominator == 0:
        return 0.0
    return numerator / denominator


def z_score(series: Sequence[float]) -> float:
    """Вычисляет z-score последнего элемента."""

    if len(series) < 2:
        return 0.0
    mean = sum(series) / len(series)
    variance = sum((x - mean) ** 2 for x in series) / (len(series) - 1)
    if variance <= 0:
        return 0.0
    std = math.sqrt(variance)
    return (series[-1] - mean) / std
