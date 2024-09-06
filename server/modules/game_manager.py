import asyncio
import random
import logging
from modules.player import Player
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.game import GameStat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self, db:AsyncSession, player1: Player, player2: Player):
        self.db = db
        self.current_player = player1
        self.opponent_player = player2
        self.task_queue = asyncio.Queue()
        self.active = True
        self.turn = 0
        


    
    async def add_task(self, task_data):
        await self.task_queue.put(task_data)

    async def process_tasks(self):
        while self.active:
            task_data = await self.task_queue.get()
            if task_data is None:
                break
            await self.handle_task(task_data)
            self.task_queue.task_done()

    async def handle_task(self, task_data):
        wait_time = random.uniform(1, 3)
        await asyncio.sleep(wait_time)
        logger.info(f"Processed task: {task_data}")

    async def stop(self):
        self.active = False
        await self.task_queue.put(None)
        await self.task_queue.join()

    async def receive_message(self, player: Player):
        try:
            while self.active:
                message = await player.websocket.receive_text()
                await self.add_task(f"Player {player.user_id}: {message}")
        except Exception as e:
            logger.error(f"Error in receiving message from Player {player.user_id}: {e}")

    async def receive_and_process_messages(self):
        await asyncio.gather(
            self.receive_message(self.current_player),
            self.receive_message(self.opponent_player)
        )
        await self.stop()

    async def handle_disconnect(self, player: Player):
        """ 플레이어의 연결이 끊겼을 때 호출됩니다. """
        logger.info(f"Player {player.user_id} disconnected from game.")
        # 여기서 게임 상태를 처리하거나, 다른 플레이어에게 알릴 수 있습니다.
        self.active = False  # 게임을 중단하려면 설정


    async def send_game_stat(self) -> GameStat:
        current_player_info = await self.current_player.get_info()
        opponent_player_info = await self.opponent_player.get_info()
        
        game_stat_current = GameStat(
            Player=current_player_info,
            opponent=opponent_player_info,
            trun=self.turn,
            is_player_turn=True
        )
        
        game_stat_opponent = GameStat(
            Player=opponent_player_info,
            opponent=current_player_info,
            trun=self.turn,
            is_player_turn=False
        )
        
        self.current_player.websocket.send_json(game_stat_current, mode="gameStat")
        self.opponent_player.websocket.send_json(game_stat_opponent,mode="gameStat")
        
    async def game_start(self):
        if random.randint(0,1):
            self.opponent_player, self.current_player = self.current_player, self.opponent_player
        await asyncio.gather(self.current_player.start(self.db),
                            self.opponent_player.start(self.db))
        self.send_game_stat()

    async def send_available_move(self):
        available_effects = await self.current_player.effect_manager.get_available_effects()