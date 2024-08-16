import asyncio
from fastapi import WebSocket


class TaskProcessor:
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.패 = []
        self.필드 = []
        self.묘지 = []
        self.덱 = []
        

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
        # 동기적으로 작업을 처리하는 부분
        print(f"Processing task: {task_data}")
        import time
        time.sleep(2)  # 동기 처리 작업 시뮬레이션
        print(f"Task completed: {task_data}")

    async def stop(self):
        await self.task_queue.put(None)
        await self.task_queue.join()
