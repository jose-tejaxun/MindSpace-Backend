from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question_id: str
    answer: str

class TestSubmit(BaseModel):
    test_id: str
    answers: List[Answer]
