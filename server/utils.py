# server/utils.py
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Request, Response, status
from server.auth import refresh_access_token, set_auth_cookies
from server.schemas.player_cards import PlayerCardReturn
import os
from dotenv import load_dotenv

from server.services.players import player_services

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
    
    
async def handle_token_refresh(db: AsyncSession, request: Request, response: Response):
    result = await refresh_access_token(db=db, request=request)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    player_id, new_access_token, new_refresh_token = result
    if new_access_token and new_refresh_token:
        await handle_transaction(db, player_services.update_refresh_token, player_id=player_id, refresh_token=new_refresh_token)
        set_auth_cookies(response=response, access_token=new_access_token, refresh_token=new_refresh_token)
    
    return player_id
