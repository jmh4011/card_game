# services/games.py

import asyncio
from fastapi import WebSocket, WebSocketDisconnect, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud import GameModCrud, UserStatCrud, UserDeckSelectionCrud
from schemas.db.game_mods import GameModSchemas
from auth import create_websocket_token
from modules.player import Player
from modules.room_manager import room_manager
import logging
from services.users import UserServices

logger = logging.getLogger(__name__)

class GameServices:

    @staticmethod
    async def get_mod(mod_id: int, db: AsyncSession) -> GameModSchemas:
        mod = await GameModCrud.get(db=db, mod_id=mod_id)
        return mod

    @staticmethod
    async def get_mods(db: AsyncSession) -> list[GameModSchemas]:
        mods = await GameModCrud.get_all(db=db)
        return mods

    @staticmethod
    async def get_token(db: AsyncSession, user_id: int):
        return await create_websocket_token(user_id)

    @staticmethod
    async def check_user(db: AsyncSession, user_id: int):
        user_stat = await UserServices.get_stat(db=db, user_id=user_id)
        if user_stat is None:
            return False
        user_deck = await UserServices.get_deck_selection(db=db, user_id=user_id, mod_id=user_stat.current_mod_id)
        if user_deck is None:
            return False
        return True

    @staticmethod
    async def connect_user(db: AsyncSession, websocket: WebSocket, user_id: int):
        try:
            user_info = await UserStatCrud.get(db=db, user_id=user_id)
            # 플레이어 매칭 시도 및 매칭될 때까지 대기
            game_manager = await room_manager.match(db=db, 
                                                    user_id=user_id, 
                                                    websocket= websocket,
                                                    mod_id=user_info.current_mod_id)

            # 게임이 진행되는 동안 웹소켓 연결 유지
            await game_manager.wait_until_game_over()

        except WebSocketDisconnect:
            logger.info(f"Client {user_id} disconnected")
            await GameServices.disconnect_user(db=db, websocket=websocket, user_id=user_id)
        except Exception as e:
            logger.error(f"Error in connect_user: {e}")
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)

    @staticmethod
    async def disconnect_user(db: AsyncSession, websocket: WebSocket, user_id: int):
        logger.info(f"Client {user_id} disconnected")
        user_info = await UserStatCrud.get(db=db, user_id=user_id)

        # 매칭 취소 또는 게임 중단 처리
        await room_manager.match_cancel(user_id=user_id, mod_id=user_info.current_mod_id)
        game_manager = await room_manager.get_active_game(user_id)

        if game_manager:
            await game_manager.handle_disconnect(user_id)
            await room_manager.unregister_game(user_id)
        await websocket.close()
        logger.info("서비스에서 닫음")

