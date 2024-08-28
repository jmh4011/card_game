from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import GameServices
from auth import get_user_id, verify_token
from schemas.game_mods import GameModSchemas
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/games/mods", response_model=list[GameModSchemas])
async def read_cards_all_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    mods = await GameServices.get_mods(db=db)
    return mods 


@router.get("/games/tokens")
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

    await websocket.accept()
    user_id: int = payload.get('uid')

    # 게임 서비스에서 유저 연결 처리
    room_id = await GameServices.connect_user(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()

            if data == "disconnect":  # 특정 조건에서 연결 종료
                await websocket.close(code=4000)  # 의도적으로 연결 종료 (코드: 4000)
                break

            # 메시지를 게임 서비스로 처리 위임
            await GameServices.handle_message(user_id, data)

    except WebSocketDisconnect:
        # 게임 서비스에서 유저 연결 해제 처리
        await GameServices.disconnect_user(user_id)
        GameServices.remove_user_from_queue(user_id)