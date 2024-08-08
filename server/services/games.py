from fastapi import FastAPI, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from crud import GameModeCrud
from schemas.game_modes import GameMode
from utils import handle_transaction, to_dict
from module import room_manager

class GameServices:
    @staticmethod
    async def get(db:AsyncSession) -> list[GameMode]:
        modes = await GameModeCrud.get_all(db=db)
        return modes


    @staticmethod
    async def matching(db:AsyncSession, user_id:int):
        room_id = room_manager.assign_room(user_id)
        return room_id
    

    @staticmethod
    async def forget_matching(db:AsyncSession, user_id:int):
        room_id = room_manager.remove_client_from_room(user_id)
        return room_id