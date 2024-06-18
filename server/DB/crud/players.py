from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from ..models import Player
from ..schemas import PlayerCreate, PlayerUpdate

async def get_player(db: AsyncSession, player_id: int):
    result = await db.execute(select(Player).filter(Player.player_id == player_id))
    return result.scalar_one_or_none()

async def create_player(db: AsyncSession, player: PlayerCreate):
    db_player = Player(**player.model_dump())
    db.add(db_player)
    await db.commit()
    await db.refresh(db_player)
    return db_player

async def update_player(db: AsyncSession, player_id: int, player: PlayerUpdate):
    db_player = await db.get(Player, player_id)
    if db_player:
        for key, value in player.model_dump().items():
            setattr(db_player, key, value)
        await db.commit()
        await db.refresh(db_player)
        return db_player
    return None

async def delete_player(db: AsyncSession, player_id: int):
    db_player = await db.get(Player, player_id)
    if db_player:
        await db.delete(db_player)
        await db.commit()
        return db_player
    return None

async def search_players(db: AsyncSession, **kwargs) -> list[Player]:
    conditions = []
    for field, value in kwargs.items():
        if field not in Player.__table__.columns.keys():
            return -1
        conditions.append(getattr(Player, field) == value)
    
    stmt = select(Player).where(and_(*conditions))
    result = await db.execute(stmt)
    db_players = result.scalars().all()
    
    return db_players
