from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    sender: str  # "user" or "bot"
    message: str
    timestamp: datetime

class ChatSession(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    messages: List[ChatMessage]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
