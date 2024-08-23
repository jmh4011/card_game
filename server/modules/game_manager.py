import asyncio
from fastapi import WebSocket
from modules.player import Player

class GameManager:
    def __init__(self, player1:Player, player2:Player):
        self.task_queue = asyncio.Queue()
        self.player1 = player1
        self.player2 = player2

    async def add_task(self, task_data):
        await self.task_queue.put(task_data)

    async def process_tasks(self):
        while True:
            task_data = await self.task_queue.get()
            if task_data is None:
                break
            self.handle_task(task_data)
            self.task_queue.task_done()

    def handle_task(self, task_data):
        pass

    async def stop(self):
        await self.task_queue.put(None)
        await self.task_queue.join()
