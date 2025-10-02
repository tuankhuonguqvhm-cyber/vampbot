"""Inline режим."""
from __future__ import annotations

from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent

router = Router(name='inline')


@router.inline()
async def inline_handler(query: InlineQuery) -> None:
    text = f"Город игрока @{query.from_user.username or 'unknown'}"
    result = InlineQueryResultArticle(
        id='city',
        title='Мой город',
        input_message_content=InputTextMessageContent(message_text=text),
        description='Поделитесь карточкой своего города',
    )
    await query.answer([result], cache_time=5)
