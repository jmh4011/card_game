# server/DB/crud/players.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from ..models import Player
from ..schemas.players import PlayerCreate, PlayerUpdate


class player_crud:
    @staticmethod
    async def get(db: AsyncSession, player_id: int) -> Player | None:
        result = await db.execute(select(Player).filter(Player.player_id == player_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, player: PlayerCreate) -> Player:
        db_player = Player(**player.model_dump())
        db.add(db_player)
        return db_player

    @staticmethod
    async def update(db: AsyncSession, player_id: int, player: PlayerUpdate) -> Player | None:
        db_player = await db.get(Player, player_id)
        if db_player:
            for key, value in player.model_dump().items():
                setattr(db_player, key, value)
            return db_player
        return None

    @staticmethod
    async def delete(db: AsyncSession, player_id: int) -> Player | None:
        db_player = await db.get(Player, player_id)
        if db_player:
            await db.delete(db_player)
            return db_player
        return None

    @staticmethod
    async def get_username(db: AsyncSession, username: str) -> Player | None:
        result = await db.execute(select(Player).filter(Player.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_refresh_token(db: AsyncSession, player_id:int, refresh_token:str):
        db_player = await db.get(Player, player_id)
        if db_player:
            db_player.refresh_token = refresh_token
        return db_player

    @staticmethod
    async def search(db: AsyncSession, **kwargs) -> list[Player] | None:
        conditions = []
        for field, value in kwargs.items():
            if field not in Player.__table__.columns.keys():
                return None
            conditions.append(getattr(Player, field) == value)
        
        stmt = select(Player).where(and_(*conditions))
        result = await db.execute(stmt)
        db_players = result.scalars().all()
        
        return db_players
