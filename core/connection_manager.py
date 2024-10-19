from typing import Dict

from fastapi import WebSocket
from core.redis import is_user_online

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



    async def send_text(self, receiver: Username, message: str):
        if await is_user_online(receiver) and receiver in self.active_connections:
            await self.active_connections[receiver].send_text(message)
        else:
            print("receiver not online")

    async def send_json(self, receiver: Username, data: dict):
        if await is_user_online(receiver) and receiver in self.active_connections:
            await self.active_connections[receiver].send_json(data)
        else:
            print("receiver not online")

    async def broadcast_send(self, data: dict):
        for username in self.active_connections:
            if await is_user_online(username):
                await self.active_connections[username].send_json(data)


manager = ConnectionManager()