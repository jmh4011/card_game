import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from auth import create_refresh_token, verify_password, create_access_token, get_password_hash
from crud import UserCrud, UserCardCrud, UserStatCrud, UserDeckSelectionCrud
from schemas.users import UserLogin, UserCreate
from schemas.user_stats import UserStatSchemas, UserStatCreate
from models import User
from schemas.user_deck_selections import UserDeckSelectionSchemas,UserDeckSelectionUpdate, UserDeckSelectionCreate
import logging

logger = logging.getLogger(__name__)


class UserServices:
    
    @staticmethod
    async def update_refresh_token(db: AsyncSession, user_id: int, refresh_token: str | None):
        try:
            user = await UserCrud.update_refresh_token(db=db,user_id=user_id, refresh_token=refresh_token)
            await db.commit()
            await db.refresh(user)
            return user
        except Exception as e:
            await db.rollback()
            raise e

    @staticmethod
    async def login(db: AsyncSession, user: UserLogin) -> tuple:
        db_user = await UserCrud.get_username(db=db, username=user.username)
        if db_user and await verify_password(user.password, db_user.password):
            access_token = await create_access_token(db_user.user_id)
            refresh_token = await create_refresh_token(db_user.user_id)
            try:
                user = await UserCrud.update_refresh_token(db=db,user_id=db_user.user_id, refresh_token=refresh_token)
                await db.commit()
                await db.refresh(user)
                return (access_token, refresh_token)    
            except Exception as e:
                await db.rollback()
                raise e
        return None
    
    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> tuple:
        if await UserCrud.get_username(db=db, username=user.username):
            return None
        user_info = UserCreate(username=user.username, password= await get_password_hash(user.password))
        try:
            db_user : User = await UserCrud.create(db=db, user=user_info)
            await db.commit()
            await db.refresh(db_user)
            access_token = await create_access_token(db_user.user_id)
            refresh_token = await create_refresh_token(db_user.user_id)
            refresh_user = await UserCrud.update_refresh_token(db= db,user_id=db_user.user_id, refresh_token=refresh_token)
            user_stat = await UserStatCrud.create(db=db, stats=UserStatCreate(user_id=db_user.user_id, nickname=db_user.username))
            await db.commit()
            await db.refresh(refresh_user)
            await db.refresh(user_stat)
            return (access_token, refresh_token)
        except Exception as e:
            await db.rollback()
            raise e
        
    @staticmethod
    async def get_stat(db: AsyncSession, user_id: int) -> UserStatSchemas:
        stat = await UserStatCrud.get(db=db, user_id=user_id)
        await db.commit()
        await db.refresh(stat)
        return stat
    
    @staticmethod
    async def get_cards(db: AsyncSession, user_id: int) -> dict[int,int]:
        cards = await UserCardCrud.get_all(db=db, user_id=user_id)
        await db.commit()
        for card in cards:
            await db.refresh(card)
        return {card.card_id:card.card_count for card in cards}
    

    @staticmethod
    async def get_deck_selection(db:AsyncSession,user_id:int) -> dict[str,int]:
        decks: list[UserDeckSelectionSchemas] = await UserDeckSelectionCrud.get_all(db=db, user_id=user_id)
        await db.commit()
        for deck in decks:
            await db.refresh(deck)
        return {deck.game_mode:deck.deck_id for deck in decks}
    
    @staticmethod
    async def set_deck_selection(db:AsyncSession,user_id:int, data:UserDeckSelectionUpdate) -> list[UserDeckSelectionSchemas]:
        deck: None|UserDeckSelectionSchemas = await UserDeckSelectionCrud.get(db=db, user_id=user_id, game_mode=data.game_mode)
        try: 
            if deck:
                result = await UserDeckSelectionCrud.update(db=db, selection_id=deck.selection_id, deck_selection=data)
            else:
                deck_selection = UserDeckSelectionCreate(user_id=user_id, game_mode=data.game_mode, deck_id=data.deck_id)
                result = await UserDeckSelectionCrud.create(db=db, deck_selection=deck_selection)
            await db.commit()
            await db.refresh(result)
            return result
        except Exception as e:
            await db.rollback()
            raise e