from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, delete
from models import UserDeckSelection
from server.schemas.user_deck_selections import UserDeckSelectionUpdate, UserDeckSelectionCreate

class UserDeckSelectionCrud:

    @staticmethod
    async def get(db: AsyncSession, user_id: int, game_mode: str):
        db_user_deck_selection = await db.execute(select(UserDeckSelection).filter_by(user_id=user_id, game_mode=game_mode))
        return db_user_deck_selection.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, deck_selection: UserDeckSelectionCreate):
        db_user_deck_selection = UserDeckSelection(**deck_selection.model_dump())
        db.add(db_user_deck_selection)
        return db_user_deck_selection

    @staticmethod
    async def update(db: AsyncSession, selection_id: int, deck_selection: UserDeckSelectionUpdate):
        db_user_deck_selection = await db.get(UserDeckSelection, selection_id)
        if db_user_deck_selection:
            for key, value in deck_selection.model_dump().items():
                setattr(db_user_deck_selection, key, value)
            return db_user_deck_selection
        return None

    @staticmethod
    async def delete(db: AsyncSession, selection_id: int):
        db_user_deck_selection = await db.get(UserDeckSelection, selection_id)
        if db_user_deck_selection:
            await db.delete(db_user_deck_selection)
            return db_user_deck_selection
        return None

    @staticmethod
    async def get_all(db: AsyncSession, user_id: int):
        result = await db.execute(select(UserDeckSelection).filter(UserDeckSelection.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def delete_all(db: AsyncSession, user_id: int):
        await db.execute(delete(UserDeckSelection).filter(UserDeckSelection.user_id == user_id))
