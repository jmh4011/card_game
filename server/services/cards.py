# server/services/cards.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..crud import card_crud
from ..schemas import cards as card_schemas
from ..models import Card

class card_services:

    @staticmethod
    async def create_card(db: AsyncSession, card: card_schemas.CardCreate) -> Card:
        return await card_crud.create(db=db, card=card)


    @staticmethod
    async def get_card(db: AsyncSession, card_id: int) -> Card:
        return await card_crud.get(db=db, card_id=card_id)

    @staticmethod
    async def update_card(db: AsyncSession, card_id: int, card: card_schemas.CardCreate) -> Card:
        return await card_crud.update(db=db, card_id=card_id, card=card)

    @staticmethod
    async def delete_card(db: AsyncSession, card_id: int) -> Card:
        return await card_crud.delete(db=db, card_id=card_id)
