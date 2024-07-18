# server/DB/crud/cards.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Card
from schemas.cards import CardCreate, CardUpdate


class card_crud:
    @staticmethod
    async def get(db: AsyncSession, card_id: int):
        db_card = await db.execute(select(Card).where(Card.card_id == card_id))
        return db_card.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card: CardCreate):
        db_card = Card(**card.model_dump())
        db.add(db_card)
        return db_card

    @staticmethod
    async def update(db: AsyncSession, card_id: int, card: CardUpdate):
        db_card = await db.get(Card, card_id)
        if db_card:
            for key, value in card.model_dump().items():
                setattr(db_card, key, value)
            return db_card
        return None

    @staticmethod
    async def delete(db: AsyncSession, card_id: int):
        db_card = await db.get(Card, card_id)
        if db_card:
            await db.delete(db_card)
            return db_card
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        db_cards = await db.execute(select(Card))
        return db_cards.scalars().all()