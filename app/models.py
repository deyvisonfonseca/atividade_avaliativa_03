from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MessageBase(BaseModel):
    """Modelo base para mensagens."""
    username: str = Field(..., max_length=50)
    content: str = Field(..., max_length=1000)

class MessageIn(MessageBase):
    """Modelo de entrada para uma nova mensagem."""
    pass

class MessageOut(MessageBase):
    """Modelo de saída para uma mensagem, incluindo ID e timestamp."""
    id: str = Field(..., alias="_id")
    room: str
    created_at: datetime