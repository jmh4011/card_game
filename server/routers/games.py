import asyncio
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from modules.game_manager import GameManager
from modules.player import Player
from services import GameServices
from auth import get_user_id, verify_token
from schemas.db.game_mods import GameModSchemas
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/games/mods/{mod_id}", response_model=GameModSchemas)
async def read_cards_all_route(mod_id:int, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    mod = await GameServices.get_mod(mod_id=mod_id, db=db)
    if mod == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found mod")
    return mod


@router.get("/games/mods", response_model=list[GameModSchemas])
async def read_cards_all_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    mods = await GameServices.get_mods(db=db)
    return mods 


@router.get("/games/tokens", response_model=str)
async def websocket_token(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    token = await GameServices.get_token(db=db, user_id=user_id)
    return token 


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload: dict[str, Any] = await verify_token(token)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    user_id: int = payload.get('uid')
    if not await GameServices.check_user(db=db, user_id=user_id):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    # 게임 서비스에서 유저 연결 처리
    await GameServices.connect_user(db=db, websocket=websocket, user_id=user_id)

    
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
        await GameServices.disconnect_user(user_id=user_id)