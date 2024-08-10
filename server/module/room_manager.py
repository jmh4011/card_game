# room_manager.py

from threading import Lock
from fastapi import WebSocket, WebSocketDisconnect

class RoomManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = {}  # 방 ID를 키로 하는 딕셔너리
        self.waiting_users = []  # 대기 중인 유저 리스트
        self.user_rooms = {}  # WebSocket 인스턴스를 키로 하고 방 ID를 값으로 하는 딕셔너리
        self.room_counter = 0
        self._lock = Lock()  # 동시성 제어를 위한 Lock

    def match_or_create_room(self, websocket: WebSocket):
        with self._lock:  # 동시성 제어
            if self.waiting_users:
                # 대기 중인 유저가 있으면 매칭하여 새로운 방 생성
                partner = self.waiting_users.pop(0)
                room_id = f"room_{self.room_counter}"
                self.room_counter += 1
                self.rooms[room_id] = [partner, websocket]
                self.user_rooms[partner] = room_id
                self.user_rooms[websocket] = room_id
                return room_id
            else:
                # 대기 중인 유저가 없으면 대기열에 추가
                self.waiting_users.append(websocket)
                return None

    def remove_client(self, websocket: WebSocket):
        with self._lock:  # 동시성 제어
            # 방 ID를 통해 클라이언트를 제거
            room_id = self.user_rooms.get(websocket)
            if room_id:
                self.rooms[room_id].remove(websocket)
                del self.user_rooms[websocket]
                if not self.rooms[room_id]:  # 방이 비었으면 제거
                    del self.rooms[room_id]

            # 대기열에서 제거
            if websocket in self.waiting_users:
                self.waiting_users.remove(websocket)

    def get_room_partners(self, websocket: WebSocket):
        # 클라이언트의 방에 있는 다른 파트너들을 반환
        room_id = self.user_rooms.get(websocket)
        if room_id:
            return [user for user in self.rooms[room_id] if user != websocket]
        return []

# 모듈 내 싱글톤 인스턴스
room_manager = RoomManager()
