# server/utils.py
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from server.DB.schemas import PlayerCardReturn
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일을 로드하여 환경 변수로 설정

SECRET_KEY = os.getenv('SECRET_KEY')

def get_secret_key():
    return SECRET_KEY


async def to_dict(instance, db: AsyncSession):
    if isinstance(instance.__class__, DeclarativeMeta):
        await db.refresh(instance)  # 비동기적으로 객체를 새로 고침
        return {c.name: getattr(instance, c.name) for c in instance.__table__.columns}
    elif isinstance(instance, dict):
        return instance
    elif isinstance(instance, PlayerCardReturn):
        return instance.model_dump()
    else:
        raise ValueError("The provided instance is not a SQLAlchemy model, dictionary, or PlayerCardReturn instance.")
    

async def handle_transaction(db: AsyncSession, func, *args, **kwargs):
    try:
        result = await func(db, *args, **kwargs)
        await db.commit()  # 명시적으로 커밋 수행
        if hasattr(result, "__await__"):
            await db.refresh(result)
        return result
    except Exception as e:
        await db.rollback()  # 오류 발생 시 롤백
        raise HTTPException(status_code=400, detail=str(e))