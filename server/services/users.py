import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from auth import create_refresh_token, verify_password, create_access_token, get_password_hash
from crud import UserCrud, UserCardCrud, UserStatCrud, UserDeckSelectionCrud, DeckCrud
from schemas.db.users import UserCreate
from schemas.db.user_stats import UserStatSchemas, UserStatCreate, UserStatUpdate
from schemas.db.decks import DeckSchemas
from schemas.router.user_stats import RouterUserStatUpdate
from schemas.db.user_deck_selections import UserDeckSelectionSchemas,UserDeckSelectionUpdate, UserDeckSelectionCreate
import logging
from schemas.router.users import UserLogin

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
            db_user = await UserCrud.create(db=db, user=user_info)
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
        await db.refresh(stat)
        return stat
    
    @staticmethod
    async def update_stat(db: AsyncSession, user_id: int, data: RouterUserStatUpdate) -> UserStatSchemas | None:
        db_stat = await UserStatCrud.get(db=db, user_id=user_id)
        if db_stat is None:
            return None

        updated_values = {
            "money": data.money if data.money is not None else db_stat.money,
            "nickname": data.nickname if data.nickname is not None else db_stat.nickname,
            "current_mod_id": data.current_mod_id if data.current_mod_id is not None else db_stat.current_mod_id
        }

        try:
            stat_info = UserStatUpdate(**updated_values)
            update_stat = await UserStatCrud.update(db=db, user_id=user_id, user_stats=stat_info)
            
            await db.commit()
            await db.refresh(update_stat)
            return update_stat
        except Exception as e:
            await db.rollback()
            raise e

    
    @staticmethod
    async def get_cards(db: AsyncSession, user_id: int) -> dict[int,int]:
        cards = await UserCardCrud.get_all(db=db, user_id=user_id)
        await db.commit()
        for card in cards:
            await db.refresh(card)
        return {card.card_id:card.card_count for card in cards}
    

    
    @staticmethod
    async def get_deck_selection(db: AsyncSession, user_id: int, mod_id: int) -> DeckSchemas | None:
        deck_selection: UserDeckSelectionSchemas = await UserDeckSelectionCrud.get(db=db, user_id=user_id, mod_id=mod_id)
        await db.commit()
        if deck_selection == None:
            return None
        await db.refresh(deck_selection)
        deck = await DeckCrud.get(db=db, deck_id=deck_selection.deck_id)
        await db.commit()
        await db.refresh(deck)
        if deck == None:
            return None
        return deck
    
    
    @staticmethod
    async def get_deck_selection_all(db:AsyncSession,user_id:int) -> dict[int,DeckSchemas]:
        deckSelections: list[UserDeckSelectionSchemas] = await UserDeckSelectionCrud.get_all(db=db, user_id=user_id)
        await db.commit()
        result = {}
        for deckSelection in deckSelections:
            await db.refresh(deckSelection)
            deck = await DeckCrud.get(db=db, deck_id=deckSelection.deck_id)
            await db.commit()
            await db.refresh(deck)
            result.update({deckSelection.mod_id:deck})
        return result
    
    @staticmethod
    async def set_deck_selection(db:AsyncSession,user_id:int, data:UserDeckSelectionUpdate) -> list[UserDeckSelectionSchemas]:
        deck: None|UserDeckSelectionSchemas = await UserDeckSelectionCrud.get(db=db, user_id=user_id, mod_id=data.mod_id)
        try: 
            if deck:
                result = await UserDeckSelectionCrud.update(db=db, selection_id=deck.selection_id, deck_selection=data)
            else:
                deck_selection = UserDeckSelectionCreate(user_id=user_id, mod_id=data.mod_id, deck_id=data.deck_id)
                result = await UserDeckSelectionCrud.create(db=db, deck_selection=deck_selection)
            await db.commit()
            await db.refresh(result)
            return result
        except Exception as e:
            await db.rollback()
            raise e