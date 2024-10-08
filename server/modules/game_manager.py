# modules/game_manager.py

import asyncio
import random
import logging
from typing import TYPE_CHECKING
from collections import deque
from modules.player import Player
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.game.enums import MessageReturnType, MessageType, MoveType
from modules.effect import Effect
from schemas.game.game_info import GameInfo
from schemas.game.message import MessageModel, MessageReturnModel
from schemas.game.move import Move, MoveReturn
from schemas.game.trigger_cards import TriggerCards
from schemas.game.effect_info import ChainInfo, EffectInfo
if TYPE_CHECKING:
    from modules.card import Card

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, db: AsyncSession, player1: Player, player2: Player):
        self.db = db
        self.turn_player = player1
        self.not_turn_player = player2
        self.move_player = player1
        self.not_move_player = player2
        self.active = True
        self.turn = 0
        self.trigger_cards = TriggerCards()
        self.side_effects: list[Effect] = []

    async def _send_message(self, player: Player, message_type: MessageType, data):
        message = MessageModel(type=message_type, data=data)
        await player.websocket.send_json(message.model_dump())

    async def receive_message(self, player: Player, timeout=30.0) -> MessageReturnModel | None:
        try:
            logger.info(f"Waiting for message from Player {player.user_id}")
            message_text = await asyncio.wait_for(player.websocket.receive_text(), timeout=timeout)
            message = MessageReturnModel.model_validate_json(message_text)
            return message
        except asyncio.TimeoutError:
            logger.warning(f"Player {player.user_id}가 {timeout}초 내에 응답하지 않았습니다.")
            if not await self.check_connection(player):
                logger.warning(f"Player {player.user_id}의 연결이 끊어졌습니다.")
                await self.handle_disconnect(player)
            else:
                logger.warning(f"Player {player.user_id}의 연결은 유지되고 있습니다.")
            return None
        except Exception as e:
            logger.error(f"Error in receiving message from Player {player.user_id}: {e}")
            await self.handle_disconnect(player)
            return None

    async def check_connection(self, player: Player) -> bool:
        try:
            # 연결 상태를 확인하기 위해 작은 메시지를 보냅니다
            await self._send_message(player=player, message_type=MessageType.PING, data=None)
            return True
        except Exception as e:
            logger.error(f"Connection check failed for Player {player.user_id}: {e}")
            return False

    async def game_start(self):
        try:
            if random.randint(0, 1):
                self.not_turn_player, self.turn_player = self.turn_player, self.not_turn_player
            await self.turn_player.start(self.db)
            await self.not_turn_player.start(self.db)

            await self.send_game_stat()
            await self.handle_turn()
        except Exception as e:
            logger.error(f"Error in game start: {e}")
        finally:
            await self.stop()

    async def send_game_stat(self):
        turn_player_info = await self.turn_player.get_info()
        not_turn_player_info = await self.not_turn_player.get_info()

        game_stat_current = GameInfo(
            player=turn_player_info,
            opponent=not_turn_player_info,
            turn=self.turn,
            is_player_turn=True,
            side_effects=self.side_effects
        )

        game_stat_opponent = GameInfo(
            player=not_turn_player_info,
            opponent=turn_player_info,
            turn=self.turn,
            is_player_turn=False,
            side_effects=self.side_effects
        )
        await self._send_message(self.turn_player, MessageType.GAME_INFO, game_stat_current)
        await self._send_message(self.not_turn_player, MessageType.GAME_INFO, game_stat_opponent)



    async def handle_turn(self):
        while self.active:
            logger.info(f"Player {self.turn_player.user_id}'s turn.")
            while True:
                if self.handle_chain():
                    break
            self.turn_player, self.not_turn_player = self.not_turn_player, self.turn_player
            self.move_player = self.turn_player
            self.not_move_player = self.not_turn_player
            self.turn += 1
            await self.send_game_stat()
        logger.info("게임이 종료되었습니다.")


    async def handle_chain(self):
        add_chain = True
        chain_effects: deque[ChainInfo] = deque([])
        while True:
            logger.info(f"Player {self.move_player.user_id}'s move.")
            available_effects = await self.send_available_move()
            message = await self.receive_message(self.turn_player,)
            if message is None:
                break  # 연결이 끊어졌을 경우 루프 종료
            if message.type == MessageReturnType.MOVE:
                result = await self.handle_move(message.data,available_effects)
                if result:
                    chain_effects.appendleft(result) 
                    self.move_player, self.not_move_player = self.not_move_player, self.move_player
                    add_chain = True
            elif message.type == MessageReturnType.CANCEL:
                if await self.handle_cancel():
                    self.move_player, self.not_move_player = self.not_move_player, self.move_player
                    if add_chain:
                        add_chain = False
                    else:
                        break
            else:
                logger.info(f"Player {self.turn_player.user_id}: {message.data}")
                # 필요에 따라 추가 처리
        
        if chain_effects == []:
            return True
        
        for chain_info in chain_effects:
            chain_info.effect.after(effect_info=chain_info.effect_info)
            
        return False


    async def handle_move(self, data: MoveReturn, available_effects: list[Effect] ):
        logger.info(f"Processing move from Player {self.turn_player.user_id}: {data}")
        effect = available_effects[data.move_index]
        effect_info = EffectInfo(opponent=self.not_move_player, targets=[effect.targets[idx] for idx in data.target])
        effect.before(effect_info=effect_info)
        
        return ChainInfo(effect=effect,effect_info=effect_info)
        # MOVE 메시지 처리 로직을 구현합니다.
        

    async def handle_cancel(self):
        logger.info(f"Player {self.turn_player.user_id}가 동작을 취소했습니다.")
        # CANCEL 메시지 처리 로직을 구현합니다.
        return True
        
        
    async def handle_disconnect(self, player: Player):
        """플레이어의 연결이 끊겼을 때 호출됩니다."""
        logger.info(f"Player {player.user_id} disconnected from game.")
        self.active = False
        # 상대 플레이어에게 알림을 보냅니다.
        await self._send_message(
            self.not_turn_player,
            MessageType.PING,
            {"message": f"Player {player.user_id} has disconnected."}
        )


    async def stop(self):
        self.active = False
        # 웹소켓 연결 닫기
        await self.turn_player.websocket.close()
        await self.not_turn_player.websocket.close()

    async def send_available_move(self) -> list[Effect]:
        available_effects:list[Effect] = await self.turn_player.get_available_effects(opponent=self.not_turn_player)
        # 현재 플레이어에게 가능한 동작을 전송하는 로직을 추가합니다.
        message = [Move(move_type=MoveType.EFFECT,
                        entity=self.move_player.card_to_entity(effect.card),
                        select=effect.select,
                        targets=[target.entity for target in effect.targets],
                        effect_id=effect.effect_id) 
                    for effect in available_effects]
        self._send_message(player=self.move_player, message_type=MessageType.MOVE, data=message)
        return available_effects
        
        
        