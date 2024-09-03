from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import UserStat
from schemas.user_stats import UserStatCreate, UserStatUpdate

class UserStatCrud:
    @staticmethod
    async def get(db: AsyncSession, user_id: int):
        db_user_stats = await db.execute(select(UserStat).filter(UserStat.user_id == user_id))
        return db_user_stats.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, stats: UserStatCreate):
        db_user_stats = UserStat(**stats.model_dump())
        db.add(db_user_stats)
        return db_user_stats

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_stats: UserStatUpdate):
        db_user_stats = await db.get(UserStat, user_id)
        if db_user_stats:
            for key, value in user_stats.model_dump().items():
                if value is not None:
                    setattr(db_user_stats, key, value)
            return db_user_stats
        return None

    @staticmethod
    async def delete_user_stats(db: AsyncSession, user_id: int):
        db_user_stats = await db.get(UserStat, user_id)
        if db_user_stats:
            await db.delete(db_user_stats)
            return db_user_stats
        return None
