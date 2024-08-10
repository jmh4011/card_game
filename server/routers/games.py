from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from module import room_manager
from services import GameServices
from auth import get_user_id
from schemas.game_modes import GameMode


router = APIRouter()

@router.get("/game-modes", response_model=GameMode)
async def read_cards_all_route(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    modes = await GameServices.get(db=db)
    return modes



@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    user_id = await get_user_id(db=db, request=request, response=response)
    if user_id is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    await websocket.accept()
    room_id = room_manager.match_or_create_room(websocket)

    # 방 ID를 클라이언트에게 전송
    if room_id:
        await websocket.send_text(f"You are connected to {room_id}")
    else:
        await websocket.send_text("Waiting for a partner...")

    try:
        while True:
            data = await websocket.receive_text()
            if data == "disconnect":  # 특정 조건에서 연결 종료
                await websocket.close(code=4000)  # 의도적으로 연결 종료 (코드: 4000)
                break

            # 방 내 다른 유저에게 메시지 전달
            partners = room_manager.get_room_partners(websocket)
            for partner in partners:
                await partner.send_text(f"User {user_id}: {data}")

    except WebSocketDisconnect:
        print(f"Client {user_id} disconnected")
        room_manager.remove_client(websocket)
        # 방 내 다른 유저에게 연결 종료 알림
        partners = room_manager.get_room_partners(websocket)
        for partner in partners:
            await partner.send_text(f"User {user_id} has disconnected.")