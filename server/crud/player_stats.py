from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import PlayerStats
from ..schemas.player_stats import PlayerStatsCreate, PlayerStatsUpdate


class player_stats_crud:
    @staticmethod
    async def get(db: AsyncSession, player_id: int):
        db_player_stats = await db.execute(select(PlayerStats).filter(PlayerStats.player_id == player_id))
        return db_player_stats.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, stats: PlayerStatsCreate):
        db_player_stats = PlayerStats(**stats.model_dump())
        db.add(db_player_stats)
        return db_player_stats

    @staticmethod
    async def update(db: AsyncSession, player_id: int, player_stats: PlayerStatsUpdate):
        db_player_stats = await db.get(PlayerStats, player_id)
        if db_player_stats:
            for key, value in player_stats.model_dump().items():
                setattr(db_player_stats, key, value)
            return db_player_stats
        return None

    @staticmethod
    async def delete_player_stats(db: AsyncSession, player_id: int):
        db_player_stats = await db.get(PlayerStats, player_id)
        if db_player_stats:
            await db.delete(db_player_stats)
            return db_player_stats
        return None
