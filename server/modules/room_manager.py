# modules/room_manager.py

import asyncio
from collections import deque, defaultdict
from modules.player import Player
from modules.game_manager import GameManager

class RoomManager:
    def __init__(self):
        self.waiting_users: defaultdict[int, deque[Player]] = defaultdict(deque)
        self.active_games: dict[int, GameManager] = {}
        self._lock = asyncio.Lock()

    async def match(self, player: Player, mod_id: int) -> tuple[Player, Player] | None:
        async with self._lock:
            self.waiting_users[mod_id].append(player)
            if len(self.waiting_users[mod_id]) >= 2:
                player1 = self.waiting_users[mod_id].popleft()
                player2 = self.waiting_users[mod_id].popleft()
                # 매칭된 플레이어들에게 알림
                await player1.notify_matched()
                await player2.notify_matched()
                return player1, player2
            return None

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
