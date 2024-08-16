from threading import Lock
from fastapi import WebSocket

class RoomManager:
    def __init__(self):
        self.rooms: dict[str, list[int]] = {}  # 방 ID를 키로 하는 딕셔너리, 값은 user_id 리스트
        self.waiting_users: list[int] = []  # 대기 중인 유저 ID 리스트
        self.user_rooms: dict[int, str] = {}  # user_id를 키로 하고 방 ID를 값으로 하는 딕셔너리
        self.websockets: dict[int, WebSocket] = {}  # user_id를 키로 하고 WebSocket 인스턴스를 값으로 하는 딕셔너리
        self.room_counter = 0
        self._lock = Lock()  # 동시성 제어를 위한 Lock

    def match_or_create_room(self, websocket: WebSocket, user_id: int):
        with self._lock:  # 동시성 제어
            self.websockets[user_id] = websocket  # 웹소켓 저장
            if self.waiting_users:
                # 대기 중인 유저가 있으면 매칭하여 새로운 방 생성
                partner_user_id = self.waiting_users.pop()
                room_id = f"room_{self.room_counter}"
                self.room_counter += 1
                self.rooms[room_id] = [partner_user_id, user_id]
                self.user_rooms[partner_user_id] = room_id
                self.user_rooms[user_id] = room_id
                return room_id
            else:
                # 대기 중인 유저가 없으면 대기열에 추가
                self.waiting_users.append(user_id)
                return None

    def remove_client(self, user_id: int):
        with self._lock:  # 동시성 제어
            # 방 ID를 통해 클라이언트를 제거
            room_id = self.user_rooms.get(user_id)
            if room_id:
                self.rooms[room_id].remove(user_id)
                del self.user_rooms[user_id]
                if not self.rooms[room_id]:  # 방이 비었으면 제거
                    del self.rooms[room_id]

            # 대기열에서 제거
            if user_id in self.waiting_users:
                self.waiting_users.remove(user_id)

            # WebSocket 삭제
            if user_id in self.websockets:
                del self.websockets[user_id]

    def get_room_partners(self, user_id: int):
        # 클라이언트의 방에 있는 다른 파트너들의 user_id를 반환
        room_id = self.user_rooms.get(user_id)
        if room_id:
            return [uid for uid in self.rooms[room_id] if uid != user_id]
        return []

    def get_websocket(self, user_id: int):
        # user_id에 해당하는 WebSocket을 반환
        return self.websockets.get(user_id)

# 모듈 내 싱글톤 인스턴스
room_manager = RoomManager()
