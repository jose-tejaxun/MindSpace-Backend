from fastapi import APIRouter, Depends
from app.services.dependencies import get_current_user

router = APIRouter()

@router.get("/test")
async def test_user(user: dict = Depends(get_current_user)):
    return {"msg": f"Hello, {user['name']}"}