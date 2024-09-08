# crud/cardeffect.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import CardEffect
from schemas.card_effects import CardEffectCreate, CardEffectUpdate


class CardEffectCrud:
    @staticmethod
    async def get(db: AsyncSession, card_effect_id: int):
        db_card_effect = await db.execute(select(CardEffect).where(CardEffect.card_effect_id == card_effect_id))
        return db_card_effect.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, card_effect: CardEffectCreate):
        db_card_effect = card_effect(**card_effect.model_dump())
        db.add(db_card_effect)
        return db_card_effect

    @staticmethod
    async def update(db: AsyncSession, card_effect_id: int, card_effect: CardEffectUpdate):
        db_card_effect = await db.get(card_effect, card_effect_id)
        if db_card_effect:
            for key, value in card_effect.model_dump().items():
                setattr(db_card_effect, key, value)
            return db_card_effect
        return None

    @staticmethod
    async def delete(db: AsyncSession, card_effect_id: int):
        db_card_effect = await db.get(CardEffect, card_effect_id)
        if db_card_effect:
            await db.delete(db_card_effect)
            return db_card_effect
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        db_card_effects = await db.execute(select(CardEffect))
        return db_card_effects.scalars().all()