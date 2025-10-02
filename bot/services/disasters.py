"""Обработка ЧП."""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict

from core.utils import rand_weighted


@dataclass
class Disaster:
    code: str
    description: str
    impact: Dict[str, int]


class DisasterService:
    def __init__(self) -> None:
        self.weights = {
            'fire': 0.2,
            'storm': 0.15,
            'drought': 0.1,
            'festival': 0.1,
            'strike': 0.05,
            'blessing': 0.05,
            'meteor': 0.01,
            'none': 0.34,
        }

    def roll(self) -> Disaster:
        code = rand_weighted(self.weights)
        table = {
            'fire': Disaster('fire', 'Пожар в жилом квартале', {'money': -500, 'happiness': -10}),
            'storm': Disaster('storm', 'Шторм повредил инфраструктуру', {'mats': -120}),
            'drought': Disaster('drought', 'Засуха в пригородах', {'energy': -10}),
            'festival': Disaster('festival', 'Городской фестиваль', {'happiness': 15}),
            'strike': Disaster('strike', 'Забастовка на заводах', {'money': -300}),
            'blessing': Disaster('blessing', 'Благотворительный вечер', {'money': 400, 'happiness': 10}),
            'meteor': Disaster('meteor', 'Падение метеорита', {'mats': -500, 'happiness': -20}),
            'none': Disaster('none', 'Спокойный день', {}),
        }
        return table[code]
