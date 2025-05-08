from fastapi import APIRouter, Depends
from app.services.dependencies import get_current_user
from app.services.crypto_service import decrypt_data

router = APIRouter()

@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    user_name = decrypt_data(user["name"])

    profile = {
        "id": str(user["_id"]),
        "name": user_name,
        "birth_date": user["birth_date"],
        "sex": user["sex"],
        "email": user["email"],
        "role": user["role"],
        "disorders": user["disorders"],
        "big_five": user["big_five"]
    }
    return profile
