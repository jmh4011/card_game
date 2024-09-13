import asyncio
import random
import logging
from typing import TYPE_CHECKING
from modules.player import Player
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.game.enums import MessageReturnType, MessageType
from modules.effect import Effect
from schemas.game.game_info import GameInfo
from schemas.game.message import MessageModel
from schemas.game.move import Move
from schemas.game.trigger_cards import TriggerCards
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
        self.chain_effects:list[Effect] = []
        self.trigger_cards = TriggerCards()
        self.tmp_available_effects:Move
        

    async def _send_message(self, player: Player, message_type: MessageType, data):
        message = MessageModel(type=message_type, data=data)
        await player.websocket.send_json(message.model_dump())

    async def receive_message(self, player: Player, timeout=3.0):
        try:
            logger.info(f"Waiting for message from Player {player.user_id}")
            message = await asyncio.wait_for(player.websocket.receive_text(), timeout=timeout)
            return message
        except asyncio.TimeoutError:
            logger.warning(f"Player {player.user_id}가 {timeout}초 내에 응답하지 않았습니다.")
            # 연결 상태를 확인하는 로직을 추가합니다.
            if not await self.check_connection(player):
                await self.handle_disconnect(player)
            else:
                # 연결은 유지되지만 응답이 없는 경우 추가 조치를 취할 수 있습니다.
                pass
            return None
        except Exception as e:
            logger.error(f"Error in receiving message from Player {player.user_id}: {e}")
            await self.handle_disconnect(player)
            return None

    async def check_connection(self, player: Player):
        try:
            # 연결 상태를 확인하기 위해 작은 메시지를 보냅니다
            await self._send_message(player=player, message_type=MessageType.PING, data=None)
            return True
        except Exception as e:
            logger.error(f"Connection check failed for Player {player.user_id}: {e}")
            return False

    async def handle_turn(self):
        while self.active:
            logger.info(f"Player {self.turn_player.user_id}'s turn.")
            
            
            message = await self.receive_message(self.turn_player)
            if message is None:
                break  # 연결이 끊어졌을 경우 루프 종료
            elif message.type == MessageReturnType.MOVE:
                pass
            elif message.type == MessageReturnType.CANCEL:
                pass
            elif message.type == MessageReturnType.END:
                pass
            else:
                logger.info(f"Player {self.turn_player.user_id}: {message.data}")
            
            await self.handle_task(f"Player {self.turn_player.user_id}: {message}")
            # 턴 교체
            self.turn_player, self.not_turn_player = self.not_turn_player, self.turn_player
            self.turn += 1
            await self.send_game_stat()

    async def handle_task(self, task_data):
        logger.info(f"Processed task: {task_data}")
        # 여기서 메시지를 실제로 처리하는 로직을 추가합니다.

    async def handle_disconnect(self, player: Player):
        """ 플레이어의 연결이 끊겼을 때 호출됩니다. """
        logger.info(f"Player {player.user_id} disconnected from game.")
        self.active = False
        # 상대 플레이어에게 알림을 보낼 수 있습니다.
        await self._send_message(self.not_turn_player, MessageType.TEXT, {"message": f"Player {player.user_id} has disconnected."})

    async def send_game_stat(self):
        turn_player_info = await self.turn_player.get_info()
        not_turn_player_info = await self.not_turn_player.get_info()

        game_stat_current = GameInfo(
            Player=turn_player_info,
            opponent=not_turn_player_info,
            trun=self.turn,
            is_player_turn=True
        )

        game_stat_opponent = GameInfo(
            Player=not_turn_player_info,
            opponent=turn_player_info,
            trun=self.turn,
            is_player_turn=False
        )
        await self._send_message(self.turn_player, MessageType.GAMEINFO, game_stat_current)
        await self._send_message(self.not_turn_player, MessageType.GAMEINFO, game_stat_opponent)

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

    async def stop(self):
        self.active = False
        # 추가적인 정리 작업이 필요하다면 여기에 작성합니다.

    async def send_available_move(self):
        available_effects = await self.turn_player.get_available_effects(opponent=self.not_turn_player)
        # 현재 플레이어에게 가능한 동작을 전송하는 로직을 추가합니다.


    async def handle_chain(self):
        pass
    #체인 트리를 넣은 queue가 있어야하고 체인을 넣을 때마다 조건 확인하고 양 플레이어가 아무 행동 안하면 역순으로 체인 처리를 한다