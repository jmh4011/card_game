# server/DB/crud/cards.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Card
from ..schemas import CardCreate

async def get_card(db: AsyncSession, card_id: int):
    stmt = select(Card).where(Card.card_id == card_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_cards(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Card).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def create_card(db: AsyncSession, card: CardCreate):
    db_card = Card(**card.model_dump())
    db.add(db_card)
    return db_card

async def update_card(db: AsyncSession, card_id: int, card: CardCreate):
    db_card = await db.get(Card, card_id)
    if db_card:
        for key, value in card.model_dump().items():
            setattr(db_card, key, value)
        return db_card
    return None

async def delete_card(db: AsyncSession, card_id: int):
    db_card = await db.get(Card, card_id)
    if db_card:
        await db.delete(db_card)
        return db_card
    return None
