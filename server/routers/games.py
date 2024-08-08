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
    try:
        while True:
            data = await websocket.receive_text()
            if data == "disconnect":  # 특정 조건에서 연결 종료
                await websocket.close(code=4000)  # 의도적으로 연결 종료 (코드: 4000)
                break
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected")