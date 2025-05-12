from pydantic import BaseModel, Field
from typing import List, Optional, Union

class Option(BaseModel):
    label: str
    value: str

class Question(BaseModel):
    id: str
    text: str
    # Puede ser lista de strings (diagnóstico) o lista de Option (MBTI)
    options: Union[List[str], List[Option]]
    correct_answer: Optional[str] = None

class TestModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    type: str  # "diagnostic" or "mbti"
    title: str
    description: str
    questions: List[Question]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
