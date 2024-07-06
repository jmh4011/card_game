# server/services/players.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from server.auth import create_refresh_token, verify_password,create_access_token, get_password_hash
from ..crud import player_crud
from ..schemas import players as player_schemas
from ..models import Player

class player_services:
    @staticmethod
    async def login(db: AsyncSession, player: player_schemas.PlayerLogin) -> tuple:
        user = await player_crud.get_username(db=db, username=player.username)
        if user and verify_password(player.password, user.password):
            access_token = create_access_token(data={"uid": user.player_id})
            refresh_token = create_refresh_token(data={"uid": user.player_id})
            try:
                await player_crud.update_refresh_token(db=db, player_id=user.player_id, refresh_token=refresh_token)
                await db.commit()
                return (access_token, refresh_token)
            except SQLAlchemyError:
                await db.rollback()
                raise "Player Login Error"
        return (None, None)
    
    async def create(db: AsyncSession, player: player_schemas.PlayerCreate) -> tuple:
        if await player_crud.get_username(db=db, username=player.username):
            return (None, None)
        player.password = get_password_hash(player.password)
        user = await player_crud.create(db=db, player=player)
        access_token = create_access_token(data={"uid": user.player_id})
        refresh_token = create_refresh_token(data={"uid": user.player_id})
        try:
            await player_crud.update_refresh_token(db=db, player_id=user.player_id, refresh_token=refresh_token)
            await db.commit()
            return (access_token, refresh_token)
        except SQLAlchemyError:
            await db.rollback()
            raise "Player Create Error"

