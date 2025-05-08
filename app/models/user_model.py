from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    birth_date: datetime
    sex: str  # "male", "female", "other"
    email: str
    hashed_password: str
    role: str = "USER"  # or "ADMIN"
    disorders: List[str] = []
    big_five: dict = {
        "openness": 0,
        "conscientiousness": 0,
        "extraversion": 0,
        "agreeableness": 0,
        "neuroticism": 0
    }
    completed_tests: List[str] = []  # ids of completed tests

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
