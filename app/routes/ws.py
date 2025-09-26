from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..database import get_database, serialize_message
from ..ws_manager import manager
from datetime import datetime, timezone
from ..models import MessageIn

router = APIRouter()

@router.websocket("/ws/{room}")
async def websocket_endpoint(ws: WebSocket, room: str):
    """
    Gerencia a conexão WebSocket para uma sala de chat,
    enviando histórico e tratando novas mensagens.
    """
    await manager.connect(room, ws)
    
    try:
        # Envia o histórico inicial de mensagens
        db = get_database()
        cursor = db["messages"].find({"room": room}).sort("_id", -1).limit(20)
        items = [serialize_message(d) async for d in cursor]
        items.reverse()
        await ws.send_json({"type": "history", "items": items})

        while True:
            payload = await ws.receive_json()
            message = MessageIn(**payload)
            
            # Valida o conteúdo da mensagem
            if not message.content.strip():
                continue

            doc = {
                "room": room,
                "username": message.username,
                "content": message.content,
                "created_at": datetime.now(timezone.utc),
            }
            
            res = await db["messages"].insert_one(doc)
            doc["_id"] = res.inserted_id
            
            await manager.broadcast(room, {"type": "message", "item": serialize_message(doc)})
            
    except WebSocketDisconnect:
        manager.disconnect(room, ws)
    except Exception as e:
        print(f"Erro na conexão WebSocket: {e}")
        manager.disconnect(room, ws)