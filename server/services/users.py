import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from auth import create_refresh_token, verify_password, create_access_token, get_password_hash
from crud import UserCrud, UserCardCrud, UserStatCrud, UserDeckSelectionCrud
from schemas.users import UserLogin, UserCreate
from schemas.user_cards import UserCardReturn
from schemas.user_stats import UserStat, UserStatCreate
from models import User
from schemas.user_deck_selections import UserDeckSelection,UserDeckSelectionUpdate, UserDeckSelectionCreate
from utils import handle_transaction, to_dict
import logging

logger = logging.getLogger(__name__)


class UserServices:
    
    @staticmethod
    async def update_refresh_token(db: AsyncSession, user_id: int, refresh_token: str | None):
        await handle_transaction(db, UserCrud.update_refresh_token, should_refresh=True, user_id=user_id, refresh_token=refresh_token)
        
    @staticmethod
    async def login(db: AsyncSession, user: UserLogin) -> tuple:
        db_user = await UserCrud.get_username(db=db, username=user.username)
        if db_user and await verify_password(user.password, db_user.password):
            access_token = await create_access_token(data={"uid": db_user.user_id})
            refresh_token = await create_refresh_token(data={"uid": db_user.user_id})
            await handle_transaction(db, UserCrud.update_refresh_token, should_refresh=True ,user_id=db_user.user_id, refresh_token=refresh_token)
            return (access_token, refresh_token)
        return None
    
    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> tuple:
        if await UserCrud.get_username(db=db, username=User.username):
            return None
        user_info = UserCreate(username=user.username, password= await get_password_hash(User.password))
        user = await handle_transaction(db, UserCrud.create, user=user_info)
        await db.refresh(user)
        access_token = await create_access_token(data={"uid": user.user_id})
        refresh_token = await create_refresh_token(data={"uid": user.user_id})
        await handle_transaction(db, UserCrud.update_refresh_token, should_refresh=True,user_id=user.user_id, refresh_token=refresh_token)
        await handle_transaction(db, UserStatCrud.create, should_refresh=True, stats=UserStatCreate(user_id=user.user_id, current_deck_id=None, money=0))
        return (access_token, refresh_token)
        
    @staticmethod
    async def get_stat(db: AsyncSession, user_id: int) -> UserStat:
        stat = await handle_transaction(db=db, func=UserStatCrud.get, user_id=user_id)
        await db.refresh(stat)
        return stat
    
    @staticmethod
    async def get_cards(db: AsyncSession, user_id: int) -> dict[int,int]:
        cards = await handle_transaction(db=db, func=UserCardCrud.get_all, user_id=user_id)
        for card in cards:
            await db.refresh(card)
        return {card.card_id:card.card_count for card in cards}
    

    @staticmethod
    async def get_deck_selection(db:AsyncSession,user_id:int) -> dict[str,int]:
        decks = await handle_transaction(db=db, func=UserDeckSelectionCrud.get_all, user_id=user_id)
        for deck in decks:
            await db.refresh(deck)
        return {deck.game_mode:deck.deck_id for deck in decks}
    
    @staticmethod
    async def set_deck_selection(db:AsyncSession,user_id:int, data:UserDeckSelectionUpdate) -> list[UserDeckSelection]:
        deck = await handle_transaction(db=db, func=UserDeckSelectionCrud.get, user_id=user_id, game_mode=data.game_mode)
        if deck:
            result = await handle_transaction(db=db, func=UserDeckSelectionCrud.update, selection_id=deck.selection_id, deck_selection=data)
        else:
            result = await handle_transaction(db=db, func=UserDeckSelectionCrud.create, deck_selection=UserDeckSelectionCreate(user_id=user_id, game_mode=data.game_mode, deck_id=data.deck_id))
        await db.refresh(result)
        return result