from typing import Dict

from fastapi import WebSocket
from core.redis import is_user_online
from core.celery_tasks import send_notify

class Username(str):
    pass

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[Username, WebSocket] = {}

    async def connect(self, username: Username, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    async def disconnect(self, username: Username):
        if username in self.active_connections:
            del self.active_connections[username]
            await self.broadcast_send({"type": "user_status", "detail": {"username": username, "status": "offline"}})

    async def send_json(self, receiver: Username, data: dict, tg_id: int | None = None):
        if await is_user_online(receiver) and receiver in self.active_connections:
            await self.active_connections[receiver].send_json(data)
        else:
            if tg_id:
                send_notify.delay(tg_id, data)

    async def broadcast_send(self, data: dict):
        for username in self.active_connections:
            if await is_user_online(username):
                await self.active_connections[username].send_json(data)


manager = ConnectionManager()