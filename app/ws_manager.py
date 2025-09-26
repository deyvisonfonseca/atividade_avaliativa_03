from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, Set

class WSManager:
    """Gerencia as salas de chat e as conexões WebSocket."""
    def __init__(self):
        self.rooms: Dict[str, Set[WebSocket]] = {}

    async def connect(self, room: str, ws: WebSocket):
        """Aceita uma nova conexão WebSocket e a adiciona a uma sala."""
        await ws.accept()
        self.rooms.setdefault(room, set()).add(ws)

    def disconnect(self, room: str, ws: WebSocket):
        """Remove uma conexão WebSocket de uma sala."""
        conns = self.rooms.get(room)
        if conns and ws in conns:
            conns.remove(ws)
            if not conns:
                self.rooms.pop(room, None)

    async def broadcast(self, room: str, payload: dict):
        """Envia uma mensagem para todas as conexões em uma sala."""
        for ws in list(self.rooms.get(room, [])):
            try:
                await ws.send_json(payload)
            except Exception:
                self.disconnect(room, ws)

manager = WSManager()