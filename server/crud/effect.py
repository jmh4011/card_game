# crud/effect.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Effect
from schemas.effects import EffectCreate, EffectUpdate


class EffectCrud:
    @staticmethod
    async def get(db: AsyncSession, effect_id: int):
        db_effect = await db.execute(select(Effect).where(Effect.effect_id == effect_id))
        return db_effect.scalar_one_or_none()
    
    @staticmethod
    async def create(db: AsyncSession, effect: EffectCreate):
        db_effect = effect(**effect.model_dump())
        db.add(db_effect)
        return db_effect

    @staticmethod
    async def update(db: AsyncSession, effect_id: int, effect: EffectUpdate):
        db_effect = await db.get(effect, effect_id)
        if db_effect:
            for key, value in effect.model_dump().items():
                setattr(db_effect, key, value)
            return db_effect
        return None

    @staticmethod
    async def delete(db: AsyncSession, effect_id: int):
        db_effect = await db.get(Effect, effect_id)
        if db_effect:
            await db.delete(db_effect)
            return db_effect
        return None
    
    @staticmethod
    async def get_all(db: AsyncSession):
        db_effects = await db.execute(select(Effect))
        return db_effects.scalars().all()