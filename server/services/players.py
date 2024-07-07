# server/services/players.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from server.auth import create_refresh_token, verify_password,create_access_token, get_password_hash
from ..crud import player_crud, player_card_crud, player_stats_crud
from ..schemas.players import PlayerLogin, PlayerCreate
from ..schemas.player_cards import PlayerCardReturn
from ..models import Player

class player_services:
    
    @staticmethod
    async def update_refresh_token(db: AsyncSession, player_id: int, refresh_token: str):
        await player_crud.update_refresh_token(db=db, player_id=player_id, refresh_token=refresh_token)
        
    @staticmethod
    async def login(db: AsyncSession, player: PlayerLogin) -> tuple:
        user = await player_crud.get_username(db=db, username=player.username)
        if user and verify_password(player.password, user.password):
            access_token = create_access_token(data={"uid": user.player_id})
            refresh_token = create_refresh_token(data={"uid": user.player_id})
            await player_crud.update_refresh_token(db=db, player_id=user.player_id, refresh_token=refresh_token)
            return (access_token, refresh_token)
        return (None, None)
    
    
    @staticmethod
    async def create(db: AsyncSession, player: PlayerCreate) -> tuple:
        if await player_crud.get_username(db=db, username=player.username):
            return (None, None)
        player.password = get_password_hash(player.password)
        user = await player_crud.create(db=db, player=player)
        access_token = create_access_token(data={"uid": user.player_id})
        refresh_token = create_refresh_token(data={"uid": user.player_id})
        await player_crud.update_refresh_token(db=db, player_id=user.player_id, refresh_token=refresh_token)
        return (access_token, refresh_token)
        
        
    @staticmethod
    async def get_stats(db: AsyncSession, player_id: int) -> list[PlayerCardReturn]:
        return await player_stats_crud.get(db=db, player_id=player_id)
    
    @staticmethod
    async def get_cards(db: AsyncSession, player_id: int):
        return await player_card_crud.get_all(db=db, player_id=player_id)