from typing import Coroutine, Any
from sqlalchemy.ext.asyncio import AsyncSession
from modules.card import Card
from schemas.cards import CardSchemas

class Card_2(Card):
    async def __init__(self, db: AsyncSession, card_id: int, card_info: CardSchemas) -> Coroutine[Any, Any, None]:
        super().__init__(db, card_id, card_info)