from typing import Any
import uuid
from fastapi import Depends, Request, Response, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user import UserCrud
from utils import (
    get_secret_key, get_jwt_algorithm, get_access_token_expire, 
    get_refresh_token_expire, handle_transaction,
    get_websocket_token_expire
)
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = get_secret_key()
ALGORITHM = get_jwt_algorithm()
ACCESS_TOKEN_EXPIRE = get_access_token_expire()
REFRESH_TOKEN_EXPIRE = get_refresh_token_expire()
WEBSOCKET_TOKEN_EXPIRE = get_websocket_token_expire()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def create_token(uid:int, expires_delta: timedelta, **kwargs):
    to_encode = kwargs.copy()
    expire = datetime.now(timezone.utc) + expires_delta  # UTC 시간대 사용
    to_encode.update({"exp": expire, "uid": uid})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_access_token(uid: int):
    return await create_token(uid=uid, expires_delta=ACCESS_TOKEN_EXPIRE)

async def create_refresh_token(uid: int):
    return await create_token(uid=uid, jti=str(uuid.uuid4()), expires_delta=REFRESH_TOKEN_EXPIRE)

async def create_websocket_token(uid: int):
    return await create_token(uid=uid, expires_delta=WEBSOCKET_TOKEN_EXPIRE)


async def verify_token(token: str):
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("uid")
        exp = payload.get("exp")

        if user_id is None:
            logger.warning("Invalid token payload")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        # 만료 시간 확인 (UTC 시간대 사용)
        if datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            logger.warning("Token has expired")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        return payload
    except JWTError:
        logger.warning("Token is invalid or expired")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

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
            payload = await verify_token(access_token)
            user_id = payload.get('uid')
            return user_id
        except HTTPException:
            pass 

    # Refresh token 검증
    payload = await verify_token(refresh_token)
    user_id = payload.get('uid')
    user = await UserCrud.get(db=db, user_id=user_id)
    if user:
        refresh_token_expiry = user.refresh_token_expiry

        if user.refresh_token == refresh_token and refresh_token_expiry > datetime.now(timezone.utc):
            # 새로운 access token 및 refresh token 생성
            new_access_token = await create_access_token(user_id)
            new_refresh_token = await create_refresh_token(user_id)
            await handle_transaction(db, UserCrud.update_refresh_token, should_refresh=True, 
                user_id=user.user_id, refresh_token=new_refresh_token)
            await set_auth_cookies(response=response, access_token=new_access_token, refresh_token=new_refresh_token)
            return user_id
        else:
            logger.warning("Invalid or expired refresh token in database")
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    logger.warning("Unauthorized access attempt")
    raise HTTPException(status_code=401, detail="Unauthorized")
