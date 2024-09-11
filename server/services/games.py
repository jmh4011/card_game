import asyncio
from fastapi import WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from crud import GameModCrud, UserStatCrud, UserDeckSelectionCrud
from services import UserServices, DeckServices
from schemas.db.game_mods import GameModSchemas
from auth import create_websocket_token
from modules.player import Player
from modules.room_manager import room_manager
from modules.game_manager import GameManager
import logging

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
    async def check_user(db: AsyncSession, user_id:int):
        user_stat = await UserServices.get_stat(db=db, user_id=user_id)
        if user_stat is None:
            return False
        user_deck = await UserServices.get_deck_selection(db=db,user_id=user_id,mod_id=user_stat.current_mod_id)
        if user_deck is None:
            return False
        return True

    @staticmethod
    async def connect_user(db: AsyncSession, websocket: WebSocket, user_id: int):
        # 유저 연결 및 매칭
        user_info = await UserStatCrud.get(db=db, user_id=user_id)
        await db.refresh(user_info)
        user_Deck = await UserDeckSelectionCrud.get(db=db, user_id=user_id, mod_id=user_info.current_mod_id)
        await db.refresh(user_Deck)
        player = Player(user_id=user_id, websocket=websocket, deck_id=user_Deck.deck_id)
        
        # 플레이어 매칭 시도
        result = await room_manager.match(player=player, mod_id=user_info.current_mod_id)
        logger.warning(f"\n\n{result}")
        if result:
            player1, player2 = result
            player1: Player
            player2: Player
            
            # GameManager 생성 및 게임 시작
            game_manager = GameManager(db=db,player1=player1, player2=player2)
            room_manager.register_game(player1.user_id, game_manager)
            room_manager.register_game(player2.user_id, game_manager)
            await game_manager.game_start()
        
        return result

    @staticmethod
    async def disconnect_user(db: AsyncSession, websocket: WebSocket, user_id: int):
        logger.info(f"Client {user_id} disconnected")
        user_info = await UserStatCrud.get(db=db, user_id=user_id)
        player = Player(user_id=user_id, websocket=websocket)
        
        # 매칭 취소 또는 게임 중단 처리
        room_manager.match_cancel(player=player, mod_id=user_info.current_mod_id)
        game_manager = await room_manager.get_active_game(user_id)
        
        if game_manager:
            await game_manager.handle_disconnect(player)
