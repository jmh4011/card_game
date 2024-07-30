import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from auth import create_refresh_token, verify_password, create_access_token, get_password_hash
from crud import PlayerCrud, PlayerCardCrud, PlayerStatsCrud
from schemas.players import PlayerLogin, PlayerCreate
from schemas.player_cards import PlayerCardReturn
from schemas.player_stats import PlayerStats, PlayerStatsCreate
from models import Player
from utils import handle_transaction, to_dict
import logging

logger = logging.getLogger(__name__)


class PlayerServices:
    
    @staticmethod
    async def update_refresh_token(db: AsyncSession, player_id: int, refresh_token: str | None):
        await handle_transaction(db, PlayerCrud.update_refresh_token, should_refresh=True, player_id=player_id, refresh_token=refresh_token)
        
    @staticmethod
    async def login(db: AsyncSession, player: PlayerLogin) -> tuple:
        user = await PlayerCrud.get_username(db=db, username=player.username)
        if user and verify_password(player.password, user.password):
            access_token = await create_access_token(data={"uid": user.player_id})
            refresh_token = await create_refresh_token(data={"uid": user.player_id})
            await handle_transaction(db, PlayerCrud.update_refresh_token, should_refresh=True ,player_id=user.player_id, refresh_token=refresh_token)
            return (access_token, refresh_token)
        return None
    
    @staticmethod
    async def create(db: AsyncSession, player: PlayerCreate) -> tuple:
        if await PlayerCrud.get_username(db=db, username=player.username):
            return None
        player_info = PlayerCreate(username=player.username, password= await get_password_hash(player.password))
        user = await handle_transaction(db, PlayerCrud.create, player=player_info)
        await db.refresh(user)
        access_token = await create_access_token(data={"uid": user.player_id})
        refresh_token = await create_refresh_token(data={"uid": user.player_id})
        await handle_transaction(db, PlayerCrud.update_refresh_token, should_refresh=True,player_id=user.player_id, refresh_token=refresh_token)
        await handle_transaction(db, PlayerStatsCrud.create, should_refresh=True, stats=PlayerStatsCreate(player_id=user.player_id, current_deck_id=None, money=0))
        return (access_token, refresh_token)
        
    @staticmethod
    async def get_stats(db: AsyncSession, player_id: int) -> PlayerStats:
        stat = await handle_transaction(db=db, func=PlayerStatsCrud.get, player_id=player_id)
        await db.refresh(stat)
        return stat
    
    @staticmethod
    async def get_cards(db: AsyncSession, player_id: int) -> dict[int,int]:
        cards = await handle_transaction(db=db, func=PlayerCardCrud.get_all, player_id=player_id)
        for card in cards:
            await db.refresh(card)
        return {card.card_id:card.card_count for card in cards}