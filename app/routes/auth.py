from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, Token
from app.schemas.user_schema import LoginRequest
from app.services.crypto_service import encrypt_data
from app.services.auth_service import hash_password, verify_password, create_access_token
from app.database import db
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    birth_date = datetime.combine(user.birth_date, datetime.min.time())

    encrypted_name = encrypt_data(user.name)

    user_dict = {
        "name": encrypted_name,
        "birth_date": birth_date,
        "sex": user.sex,
        "email": user.email,
        "hashed_password": hashed_pw,
        "role": "USER",
        "disorders": [],
        "big_five": {
            "openness": 0,
            "conscientiousness": 0,
            "extraversion": 0,
            "agreeableness": 0,
            "neuroticism": 0
        },
        "completed_tests": []
    }

    result = await db.users.insert_one(user_dict)
    access_token = create_access_token(data={"sub": str(result.inserted_id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login(login_req: LoginRequest):
    user = await db.users.find_one({"email": login_req.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(login_req.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": str(user["_id"]), "role": user["role"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
