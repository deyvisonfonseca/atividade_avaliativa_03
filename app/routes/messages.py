from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from ..database import get_database, serialize_message
from ..models import MessageIn, MessageOut
from datetime import datetime, timezone

router = APIRouter()

@router.get("/rooms/{room}/messages", response_model=dict)
async def get_messages(
    room: str,
    limit: int = Query(20, ge=1, le=100),
    before_id: str | None = Query(None)
):
    """
    Recupera o histórico de mensagens de uma sala.
    Retorna 400 Bad Request se o ID for inválido.
    """
    query = {"room": room}
    if before_id:
        try:
            query["_id"] = {"$lt": ObjectId(before_id)}
        except Exception:
            raise HTTPException(status_code=400, detail="ID da mensagem inválido.")

    db = get_database()
    cursor = db["messages"].find(query).sort("_id", -1).limit(limit)
    docs = [serialize_message(d) async for d in cursor]
    docs.reverse()
    
    next_cursor = docs[0]["_id"] if docs else None
    
    return {"items": docs, "next_cursor": next_cursor}

@router.post("/rooms/{room}/messages", response_model=MessageOut, status_code=201)
async def post_message(room: str, message: MessageIn):
    """
    Envia uma nova mensagem para uma sala.
    A validação de conteúdo vazio é feita pelo Pydantic, mas um controle extra garante.
    """
    if not message.content.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")
    
    doc = {
        "room": room,
        "username": message.username,
        "content": message.content,
        "created_at": datetime.now(timezone.utc),
    }

    db = get_database()
    res = await db["messages"].insert_one(doc)
    doc["_id"] = res.inserted_id
    
    # Você pode adicionar um broadcast aqui se a rota REST precisar notificar os clientes WS
    # from ..ws_manager import manager
    # await manager.broadcast(room, {"type": "message", "item": serialize_message(doc)})
    
    return serialize_message(doc)