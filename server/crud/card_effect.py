# crud/cardeffect.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import CardEffect
from schemas.card_effects import CardEffectCreate, CardEffectUpdate


class cardEffectCrud:
    @staticmethod
    async def get(db: AsyncSession, cardeffect_id: int):
        db_cardeffect = await db.execute(select(CardEffect).where(CardEffect.cardeffect_id == cardeffect_id))
        return db_cardeffect.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, cardeffect: CardEffectCreate):
        db_cardeffect = cardeffect(**cardeffect.model_dump())
        db.add(db_cardeffect)
        return db_cardeffect

    @staticmethod
    async def update(db: AsyncSession, cardeffect_id: int, cardeffect: CardEffectUpdate):
        db_cardeffect = await db.get(cardeffect, cardeffect_id)
        if db_cardeffect:
            for key, value in cardeffect.model_dump().items():
                setattr(db_cardeffect, key, value)
            return db_cardeffect
        return None

    @staticmethod
    async def delete(db: AsyncSession, cardeffect_id: int):
        db_cardeffect = await db.get(CardEffect, cardeffect_id)
        if db_cardeffect:
            await db.delete(db_cardeffect)
            return db_cardeffect
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        db_cardeffects = await db.execute(select(CardEffect))
        return db_cardeffects.scalars().all()