from fastapi import APIRouter, Depends
from app.services.dependencies import get_current_admin
from app.database import db
from datetime import datetime
import pandas as pd
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

@router.get("/dashboard")
async def admin_dashboard(admin: dict = Depends(get_current_admin)):
    user_count = await db.users.count_documents({"role": "USER"})
    diagnostic_count = await db.users.count_documents({"completed_tests": {"$in": ["diagnostic"]}})
    personality_count = await db.users.count_documents({"completed_tests": {"$in": ["personality"]}})

    return {
        "total_users": user_count,
        "users_completed_diagnostic": diagnostic_count,
        "users_completed_personality": personality_count
    }

@router.get("/users")
async def get_users(admin: dict = Depends(get_current_admin)):
    users_cursor = db.users.find({"role": "USER"})
    users = []
    async for user in users_cursor:
        birth_date = user.get("birth_date")
        age = None
        if birth_date:
            birth_date = birth_date if isinstance(birth_date, datetime) else datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S")
            age = (datetime.utcnow() - birth_date).days // 365

        users.append({
            "id": str(user["_id"]),
            "age": age,
            "sex": user["sex"],
            "disorders": user["disorders"],
            "big_five": user["big_five"]
        })
    return {"users": users}

@router.get("/users/report")
async def download_users_report(admin: dict = Depends(get_current_admin)):
    users_cursor = db.users.find({"role": "USER"})
    data = []
    async for user in users_cursor:
        birth_date = user.get("birth_date")
        age = None
        if birth_date:
            birth_date = birth_date if isinstance(birth_date, datetime) else datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S")
            age = (datetime.utcnow() - birth_date).days // 365

        data.append({
            "ID": str(user["_id"]),
            "Age": age,
            "Sex": user["sex"],
            "Disorders": ", ".join(user["disorders"]),
            "Openness": user["big_five"]["openness"],
            "Conscientiousness": user["big_five"]["conscientiousness"],
            "Extraversion": user["big_five"]["extraversion"],
            "Agreeableness": user["big_five"]["agreeableness"],
            "Neuroticism": user["big_five"]["neuroticism"]
        })

    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Users')
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="users_report.xlsx"'
    }

    return StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)
