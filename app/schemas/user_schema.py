from pydantic import BaseModel, EmailStr, constr
from typing import Optional, List
from datetime import date

class UserCreate(BaseModel):
    name: str
    birth_date: date
    sex: constr(pattern="^(male|female|other)$")
    email: EmailStr
    password: constr(min_length=6)

class UserResponse(BaseModel):
    id: str
    name: str
    birth_date: date
    sex: str
    email: EmailStr
    role: str
    disorders: List[str]
    big_five: dict

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
