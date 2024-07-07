import uuid
from fastapi import Depends, Request, Response, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from server.crud.player import player_crud
from .utils import get_secret_key

SECRET_KEY = get_secret_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def set_auth_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict"
    )

async def refresh_access_token(db: AsyncSession, request: Request) -> int | None:
    try:
        access_token = request.cookies.get("access_token")
        if access_token:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("uid")
    except JWTError:
        pass

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return None

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        player_id = payload.get("uid")
        user = await player_crud.get(db, player_id)
        if user and user.refresh_token == refresh_token:
            new_access_token = create_access_token(data={"uid": player_id})
            new_refresh_token = create_refresh_token(data={"uid": player_id})
            await player_crud.update_refresh_token(db=db, player_id=player_id, refresh_token=new_refresh_token)
            return player_id, new_access_token, new_refresh_token
    except JWTError:
        return None
