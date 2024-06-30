# server/services/players.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..DB.crud import players as crud_players
from ..DB.schemas import PlayerCreate, PlayerUpdate
from ..DB.models import Player

async def create_player(db: AsyncSession, player: PlayerCreate) -> Player:
    return await crud_players.create_player(db=db, player=player)

async def get_player(db: AsyncSession, player_id: int) -> Player:
    return await crud_players.get_player(db=db, player_id=player_id)

async def get_player_by_username(db: AsyncSession, username: str) -> Player:
    return await crud_players.get_player_by_username(db=db, username=username)

async def update_player(db: AsyncSession, player_id: int, player: PlayerUpdate) -> Player:
    return await crud_players.update_player(db=db, player_id=player_id, player=player)

async def delete_player(db: AsyncSession, player_id: int) -> Player:
    return await crud_players.delete_player(db=db, player_id=player_id)

async def search_players(db: AsyncSession, **kwargs) -> list[Player]:
    return await crud_players.search_players(db=db, **kwargs)
