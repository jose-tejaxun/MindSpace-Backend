from pydantic import BaseModel, Field
from typing import List, Optional

class Question(BaseModel):
    id: str
    text: str
    options: List[str]
    correct_answer: Optional[str] = None  # for mental disorder test

class TestModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    type: str  # "disorder" or "personality"
    title: str
    description: str
    questions: List[Question]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
