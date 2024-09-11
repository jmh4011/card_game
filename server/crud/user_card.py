from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, delete
from models import UserCard
from schemas.db.user_cards import UserCardCreate, UserCardUpdate

class UserCardCrud:

    @staticmethod
    async def get(db: AsyncSession, user_id: int, card_id: int):
        db_user_card = await db.execute(select(UserCard).filter_by(user_id=user_id, card_id=card_id))
        return db_user_card.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_card: UserCardCreate):
        db_user_card = UserCard(**user_card.model_dump())
        db.add(db_user_card)
        return db_user_card

    @staticmethod
    async def update(db: AsyncSession, user_card_id: int, user_card: UserCardUpdate):
        db_user_card = await db.get(UserCard, user_card_id)
        if db_user_card:
            for key, value in user_card.model_dump().items():
                setattr(db_user_card, key, value)
            return db_user_card
        return None

    @staticmethod
    async def delete(db: AsyncSession, user_card_id: int):
        user_card = await db.get(UserCard, user_card_id)
        if user_card:
            await db.delete(user_card)
            return user_card
        return None

    @staticmethod
    async def get_all(db: AsyncSession, user_id: int):
        result = await db.execute(select(UserCard).filter(UserCard.user_id == user_id))
        return result.scalars().all()

    @staticmethod
    async def delete_all(db: AsyncSession, user_id: int):
        await db.execute(delete(UserCard).filter(UserCard.user_id == user_id))

    @staticmethod
    async def add(db: AsyncSession, user_id: int, card_id: int):
        db_user_card = await db.execute(select(UserCard).filter_by(user_id=user_id, card_id=card_id))
        existing_card = db_user_card.scalar_one_or_none()
        if existing_card:
            existing_card.card_count += 1
            return existing_card
        else:
            new_card = UserCard(user_id=user_id, card_id=card_id, card_count=1)
            db.add(new_card)
            return new_card

    @staticmethod
    async def sub(db: AsyncSession, user_id: int, card_id: int):
        db_user_card = await db.execute(select(UserCard).filter_by(user_id=user_id, card_id=card_id))
        existing_card = db_user_card.scalar_one_or_none()
        if existing_card:
            if existing_card.card_count > 1:
                existing_card.card_count -= 1
                return existing_card
            else:
                await db.execute(delete(UserCard).filter_by(user_id=user_id, card_id=card_id))
                return None

    @staticmethod
    async def search_users(db: AsyncSession, **kwargs) -> list[UserCard] | None:
        conditions = []
        for field, value in kwargs.items():
            if field not in UserCard.__table__.columns.keys():
                return None
            conditions.append(getattr(UserCard, field) == value)
        
        stmt = select(UserCard).where(and_(*conditions))
        result = await db.execute(stmt)
        db_users = result.scalars().all()
        
        return db_users
