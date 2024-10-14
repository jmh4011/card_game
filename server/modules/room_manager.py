# modules/room_manager.py

import asyncio
from collections import deque, defaultdict
from sqlalchemy.ext.asyncio import AsyncSession
from modules.player import Player
from modules.game_manager import GameManager

class RoomManager:
    def __init__(self):
        self.waiting_users: defaultdict[int, deque[Player]] = defaultdict(deque)
        self.active_games: dict[int, GameManager] = {}
        self._lock = asyncio.Lock()
        self._conditions: defaultdict[int, asyncio.Condition] = defaultdict(lambda: asyncio.Condition())

    async def match(self,db:AsyncSession, player: Player, mod_id: int) -> GameManager:
        condition = self._conditions[mod_id]
        async with condition:
            self.waiting_users[mod_id].append(player)
            if len(self.waiting_users[mod_id]) >= 2:
                player1 = self.waiting_users[mod_id].popleft()
                player2 = self.waiting_users[mod_id].popleft()

                # GameManager 생성 및 게임 시작
                game_manager = GameManager(db=db, player1=player1, player2=player2)
                await self.register_game(player1.user_id, game_manager)
                await self.register_game(player2.user_id, game_manager)

                # 게임을 별도의 태스크로 시작
                asyncio.create_task(game_manager.game_start())

                # 대기 중인 모든 플레이어에게 매칭이 완료되었음을 알림
                condition.notify_all()

                return game_manager
            else:
                # 매칭될 때까지 대기
                await condition.wait()
                # 매칭이 완료되면 게임 매니저 반환
                return self.active_games.get(player.user_id)

    async def match_cancel(self, player: Player, mod_id: int):
        async with self._lock:
            if player in self.waiting_users[mod_id]:
                self.waiting_users[mod_id].remove(player)

    async def register_game(self, user_id: int, game_manager: GameManager):
        async with self._lock:
            self.active_games[user_id] = game_manager

    async def unregister_game(self, user_id: int):
        async with self._lock:
            if user_id in self.active_games:
                del self.active_games[user_id]

    async def get_active_game(self, user_id: int) -> GameManager | None:
        async with self._lock:
            return self.active_games.get(user_id, None)

# 싱글톤 인스턴스
room_manager = RoomManager()
