from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models import PlayerStats
from ..schemas import PlayerStatsCreate

async def get_player_stats(db: AsyncSession, player_id: int):
    result = await db.execute(select(PlayerStats).filter(PlayerStats.player_id == player_id))
    return result.scalar_one_or_none()

async def create_player_stats(db: AsyncSession, stats: PlayerStatsCreate):
    db_stats = PlayerStats(**stats.model_dump())
    db.add(db_stats)

async def update_player_stats(db: AsyncSession, player_id: int, stats: PlayerStatsCreate):
    db_stats = await db.execute(select(PlayerStats).filter(PlayerStats.player_id == player_id))
    db_stats = db_stats.scalar_one_or_none()
    if db_stats:
        for key, value in stats.model_dump().items():
            setattr(db_stats, key, value)

async def delete_player_stats(db: AsyncSession, player_id: int):
    db_stats = await db.execute(select(PlayerStats).filter(PlayerStats.player_id == player_id))
    db_stats = db_stats.scalar_one_or_none()
    if db_stats:
        await db.delete(db_stats)
