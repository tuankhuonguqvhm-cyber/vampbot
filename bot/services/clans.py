"""Клановые функции."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from repositories.clans_repo import ClansRepository


@dataclass
class ClanInfo:
    id: int
    name: str
    tag: str
    members: List[Dict[str, str]]


class ClanService:
    def __init__(self, repo: ClansRepository) -> None:
        self.repo = repo

    async def create(self, leader_id: int, name: str, tag: str) -> int:
        return await self.repo.create(leader_id, name, tag)

    async def info(self, clan_id: int) -> ClanInfo:
        members = await self.repo.members(clan_id)
        return ClanInfo(id=clan_id, name=f"Клан #{clan_id}", tag=f"TAG{clan_id}", members=members)
