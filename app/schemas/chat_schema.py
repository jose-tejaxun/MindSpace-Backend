from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageInput(BaseModel):
    message: str

class MessageResponse(BaseModel):
    sender: str
    message: str
    timestamp: datetime

class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: List[MessageResponse]
