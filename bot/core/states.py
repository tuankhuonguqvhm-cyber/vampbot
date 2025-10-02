"""FSM состояния для онбординга и мастер-сцен."""
from __future__ import annotations

from aiogram.fsm.state import State, StatesGroup


class Onboarding(StatesGroup):
    choose_city = State()
    place_buildings = State()
    tutorial = State()


class BuildWizard(StatesGroup):
    choose_category = State()
    choose_building = State()
    confirm = State()


class MarketWizard(StatesGroup):
    choose_side = State()
    choose_resource = State()
    choose_amount = State()
    choose_price = State()
    confirm = State()


class ClanWizard(StatesGroup):
    name = State()
    rules = State()
    link_chat = State()


class DuelWizard(StatesGroup):
    format = State()
    opponent = State()
    confirm = State()
