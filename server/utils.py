from datetime import timedelta
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
REFRESH_TOKEN_EXPIRE = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
WEBSOCKET_TOKEN_EXPIRE = timedelta(days=int(os.getenv("WEBSOCKET_TOKEN_EXPIRE_MIUTES")))


def get_secret_key():
    return SECRET_KEY

def get_jwt_algorithm():
    return JWT_ALGORITHM

def get_access_token_expire():
    return ACCESS_TOKEN_EXPIRE

def get_refresh_token_expire():
    return REFRESH_TOKEN_EXPIRE

def get_websocket_token_expire():
    return WEBSOCKET_TOKEN_EXPIRE

async def to_dict(instance, db: AsyncSession):
    if isinstance(instance.__class__, DeclarativeMeta):
        await db.refresh(instance)
        return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    else:
        try:
            return dict(instance)
        except TypeError:
            try:
                return vars(instance)
            except TypeError:
                return instance

# async def handle_transaction(db: AsyncSession, func, *args, should_refresh=False, **kwargs) -> any:
#     try:
#         result = await func(db, *args, **kwargs)
#         await db.commit()
#         if should_refresh and result is not None:
#             if isinstance(result, list):
#                 for instance in result:
#                     await db.refresh(instance)
#             else:
#                 await db.refresh(result)
#         return result
#     except Exception as e:
#         await db.rollback()
#         raise e
