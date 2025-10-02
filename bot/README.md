# Городской Рывок+

"Городской Рывок+" — масштабная текстовая игра-менеджер города, реализованная в виде Telegram-бота на основе `aiogram 3`. Проект предназначен для демонстрации комплексной архитектуры бота, офлайн-тик-системы экономики, расширенного набора игровых механик и богатых сидов данных.

## Запуск проекта

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Скопируйте файл `.env.example` в `.env` и заполните значения:
   ```bash
   cp .env.example .env
   ```
3. Запустите бота:
   ```bash
   python main.py
   ```

### Необходимые переменные окружения

- `BOT_TOKEN` — токен бота Telegram, полученный у [@BotFather](https://t.me/BotFather).
- `ADMIN_IDS` — список ID администраторов через запятую.
- `LOG_LEVEL` — уровень логирования (`INFO`, `DEBUG`, `WARNING`).

## Структура проекта

```
bot/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── core/
│   ├── db.py
│   ├── models.py
│   ├── states.py
│   ├── utils.py
│   ├── middlewares.py
│   ├── filters.py
│   ├── security.py
│   └── texts.py
├── data/
│   ├── buildings.json
│   ├── cities_ru.json
│   ├── quests_daily.json
│   ├── quests_weekly.json
│   ├── achievements.json
│   ├── events.json
│   ├── research.json
│   ├── policies.json
│   ├── landmarks.json
│   ├── titles.json
│   └── promo_codes.json
├── repositories/
│   ├── users_repo.py
│   ├── cities_repo.py
│   ├── buildings_repo.py
│   ├── inventory_repo.py
│   ├── research_repo.py
│   ├── policies_repo.py
│   ├── achievements_repo.py
│   ├── quests_repo.py
│   ├── seasons_repo.py
│   ├── leaderboard_repo.py
│   ├── market_repo.py
│   ├── clans_repo.py
│   ├── referrals_repo.py
│   └── audit_repo.py
├── services/
│   ├── ticks.py
│   ├── buildings.py
│   ├── research.py
│   ├── policies.py
│   ├── happiness.py
│   ├── disasters.py
│   ├── quests.py
│   ├── achievements.py
│   ├── seasons.py
│   ├── leaderboard.py
│   ├── market.py
│   ├── crafting.py
│   ├── clans.py
│   ├── duels.py
│   ├── referrals.py
│   ├── reports.py
│   ├── scheduler.py
│   └── anticheat.py
├── handlers/
│   ├── start.py
│   ├── menu.py
│   ├── city.py
│   ├── build.py
│   ├── research.py
│   ├── policies.py
│   ├── clans.py
│   ├── market.py
│   ├── crafting.py
│   ├── disasters.py
│   ├── quests.py
│   ├── achievements.py
│   ├── duels.py
│   ├── referrals.py
│   ├── leaderboard.py
│   ├── inline.py
│   ├── settings.py
│   ├── admin.py
│   ├── help.py
│   └── errors.py
├── keyboards/
│   ├── common.py
│   ├── menu.py
│   ├── build.py
│   ├── research.py
│   ├── policies.py
│   ├── clans.py
│   ├── market.py
│   ├── quests.py
│   ├── achievements.py
│   ├── leaderboard.py
│   └── duels.py
├── scripts/
│   ├── manage.py
│   └── simulate.py
└── tests/
    ├── test_ticks.py
    ├── test_buildings.py
    ├── test_market.py
    ├── test_quests.py
    ├── test_achievements.py
    └── test_anticheat.py
```

## Основные возможности

- Экономика с офлайн-тик-системой, регенерацией энергии и активацией строек.
- Более сотни типов зданий, уникальные ландмарки и апгрейды.
- Исследования и политики с модификаторами доходов, лимитов и событий.
- Поддержка кланов, кооперативных мегапроектов и голосований.
- Биржа ресурсов и P2P-торговля с эскроу и комиссией.
- Дуэли, рейтинги, квесты, достижения, события и сезонный прогресс.
- Античит, rate limit, идемпотентность, журнал аудита.
- Inline-режим для шаринга карточек города и клана.
- CLI-скрипты для управления базой и симуляции экономики.

## Тестирование

В проекте присутствуют модульные тесты на базе стандартной библиотеки `unittest`. Запуск:

```bash
python -m unittest discover -s tests
```

## Соглашения по стилю

- Код следует стандарту PEP 8 и активно использует аннотации типов.
- Докстринги описывают назначение модулей и публичных функций.
- Все взаимодействия с базой данных проходят через слои репозиториев и сервисов.
- Вся пользовательская коммуникация ведётся на русском языке с `parse_mode=HTML`.

## Отказ от ответственности

Проект разработан в демонстрационных целях и не претендует на полноту коммерческого продукта. Несмотря на большое количество контента и сложную игровую логику, используйте бота как пример архитектуры и подходов к построению крупных Telegram-игр.
