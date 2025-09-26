from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Optional, Dict, Any
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URL)
db = client.get_database("deyvison")  

# --- DB helpers ---
_client: Optional[AsyncIOMotorClient] = None

def get_database():
    """Retorna o cliente de banco de dados do MongoDB."""
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(settings.MONGO_URL)
    return _client[settings.MONGO_DB]

def serialize_message(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serializa um documento do MongoDB para um formato JSON.
    Converte ObjectId e datetime para strings.
    """
    d = dict(doc)
    if "_id" in d and isinstance(d["_id"], ObjectId):
        d["_id"] = str(d["_id"])
    if "created_at" in d:
        d["created_at"] = d["created_at"].isoformat()
    return d