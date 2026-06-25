from typing import Dict, List
from fastapi import WebSocket
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        # business_id -> list of active connections
        self.active_connections: Dict[UUID, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, business_id: UUID):
        await websocket.accept()
        if business_id not in self.active_connections:
            self.active_connections[business_id] = []
        self.active_connections[business_id].append(websocket)

    def disconnect(self, websocket: WebSocket, business_id: UUID):
        if business_id in self.active_connections:
            self.active_connections[business_id].remove(websocket)

    async def broadcast_to_business(self, business_id: UUID, message: dict):
        if business_id in self.active_connections:
            for connection in self.active_connections[business_id]:
                await connection.send_json(message)

manager = ConnectionManager()
