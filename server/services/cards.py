# server/services/cards.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..DB.crud import cards as crud_cards
from ..DB.schemas import CardCreate
from ..DB.models import Card

async def create_card(db: AsyncSession, card: CardCreate) -> Card:
    return await crud_cards.create_card(db=db, card=card)

async def get_cards(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[Card]:
    return await crud_cards.get_cards(db=db, skip=skip, limit=limit)

async def get_card(db: AsyncSession, card_id: int) -> Card:
    return await crud_cards.get_card(db=db, card_id=card_id)

async def update_card(db: AsyncSession, card_id: int, card: CardCreate) -> Card:
    return await crud_cards.update_card(db=db, card_id=card_id, card=card)

async def delete_card(db: AsyncSession, card_id: int) -> Card:
    return await crud_cards.delete_card(db=db, card_id=card_id)
