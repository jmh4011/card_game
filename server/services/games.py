from fastapi import FastAPI, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from crud import GameModeCrud
from schemas.game_modes import GameModeSchemas
from auth import create_websocket_token
from utils import handle_transaction, to_dict
from modules import room_manager
import logging

logger = logging.getLogger(__name__)


class GameServices:
    @staticmethod
    async def get_mode(db:AsyncSession) -> list[GameModeSchemas]:
        modes = await GameModeCrud.get_all(db=db)
        return modes


    @staticmethod
    async def get_token(db:AsyncSession, user_id):
        return await create_websocket_token(user_id)

    @staticmethod
    async def connect_user(websocket: WebSocket, user_id: int):
        # 유저 연결 및 매칭
        room_id = room_manager.match_or_create_room(websocket, user_id)
        logger.info(f"User {user_id} connected to room: {room_id}")
        return room_id

    @staticmethod
    async def handle_message(user_id: int, data: str):
        # 메시지를 방 내 다른 유저들에게 전달
        partner_ids = room_manager.get_room_partners(user_id)
        for partner_id in partner_ids:
            partner_websocket = room_manager.get_websocket(partner_id)
            if partner_websocket:
                await partner_websocket.send_text(f"User {user_id}: {data}")

    @staticmethod
    async def disconnect_user(user_id: int):
        # 유저 연결 해제 및 방 정보 업데이트
        logger.info(f"Client {user_id} disconnected")
        room_manager.remove_client(user_id)
        # 방 내 다른 유저에게 연결 종료 알림
        partner_ids = room_manager.get_room_partners(user_id)
        for partner_id in partner_ids:
            partner_websocket = room_manager.get_websocket(partner_id)
            if partner_websocket:
                await partner_websocket.send_text(f"User {user_id} has disconnected.")
        
    @staticmethod
    def remove_user_from_queue(user_id: int):
        # 대기열에서 유저 제거
        if user_id in room_manager.waiting_users:
            room_manager.waiting_users.remove(user_id)
            logger.info(f"User {user_id} removed from the waiting queue.")