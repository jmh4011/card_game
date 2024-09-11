# /crud/users.py
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from models import User
from schemas.db.users import UserCreate, UserUpdate
from utils import get_refresh_token_expire


REFRESH_TOKEN_EXPIRE = get_refresh_token_expire()

class UserCrud:
    @staticmethod
    async def get(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).filter(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        return db_user

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user: UserUpdate) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            for key, value in user.model_dump().items():
                setattr(db_user, key, value)
            return db_user
        return None

    @staticmethod
    async def delete(db: AsyncSession, user_id: int) -> User | None:
        db_user = await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            return db_user
        return None

    @staticmethod
    async def get_username(db: AsyncSession, username: str) -> User | None:
        result = await db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_refresh_token(db: AsyncSession, user_id: int, refresh_token: str, refresh_token_expiry:timedelta = REFRESH_TOKEN_EXPIRE):
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = refresh_token
            db_user.refresh_token_expiry = datetime.now(timezone.utc) + refresh_token_expiry
        return db_user

    @staticmethod
    async def search(db: AsyncSession, **kwargs) -> list[User] | None:
        conditions = []
        for field, value in kwargs.items():
            if field not in User.__table__.columns.keys():
                return None
            conditions.append(getattr(User, field) == value)
        
        stmt = select(User).where(and_(*conditions))
        result = await db.execute(stmt)
        db_users = result.scalars().all()
        
        return db_users
