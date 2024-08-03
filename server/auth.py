import uuid
from fastapi import Depends, Request, Response, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import UserCrud
from utils import (
    get_secret_key, get_jwt_algorithm, get_access_token_expire, 
    get_refresh_token_expire, handle_transaction
)
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = get_secret_key()
ALGORITHM = get_jwt_algorithm()
ACCESS_TOKEN_EXPIRE = get_access_token_expire()
REFRESH_TOKEN_EXPIRE = get_refresh_token_expire()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def create_access_token(data: dict, expires_delta: timedelta = ACCESS_TOKEN_EXPIRE):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: timedelta = REFRESH_TOKEN_EXPIRE):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=int(ACCESS_TOKEN_EXPIRE.total_seconds())  # 쿠키 만료 시간 설정
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=int(REFRESH_TOKEN_EXPIRE.total_seconds())  # 쿠키 만료 시간 설정
    )

async def get_user_id(db: AsyncSession, request: Request, response: Response) -> int:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        logger.warning("Missing refresh token")
        raise HTTPException(status_code=401, detail="Missing refresh token")
    
    if access_token:
        try:
            # Access token 검증
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            player_id = payload.get("uid")
            if not player_id:
                logger.warning("Invalid access token payload")
                raise HTTPException(status_code=401, detail="Invalid access token")
            return player_id
        except JWTError:
            logger.warning("Access token is invalid or expired")
            pass  # Access token이 유효하지 않으면 refresh token으로 재발급 시도

    try:
        # Refresh token 검증
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        player_id = payload.get("uid")
        if not player_id:
            logger.warning("Invalid refresh token payload")
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user = await UserCrud.get(db=db, player_id=player_id)
        if user:
            refresh_token_expiry = user.refresh_token_expiry
            if refresh_token_expiry.tzinfo is None:
                # refresh_token_expiry가 timezone-naive이면 UTC로 설정
                refresh_token_expiry = refresh_token_expiry.replace(tzinfo=timezone.utc)
                
            if user.refresh_token == refresh_token and refresh_token_expiry > datetime.now(timezone.utc):
                # 새로운 access token 및 refresh token 생성
                new_access_token = await create_access_token(data={"uid": player_id})
                new_refresh_token = await create_refresh_token(data={"uid": player_id})
                await handle_transaction(db, UserCrud.update_refresh_token, should_refresh=True, 
                    player_id=user.player_id, refresh_token=new_refresh_token)
                await set_auth_cookies(response=response, access_token=new_access_token, refresh_token=new_refresh_token)
                return player_id
            else:
                logger.warning("Invalid or expired refresh token in database")
                raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    except JWTError:
        logger.warning("Refresh token is invalid or expired")
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    logger.warning("Unauthorized access attempt")
    raise HTTPException(status_code=401, detail="Unauthorized")
