from fastapi import APIRouter, Depends, HTTPException
from app.services.dependencies import get_current_user
from app.schemas.test_schema import TestSubmit
from app.database import db
from app.models.test_model import TestModel
from bson import ObjectId

router = APIRouter(prefix="/tests", tags=["Tests"])

@router.get("/{test_type}")
async def get_test_questions(test_type: str):
    """
    Obtiene las preguntas del test según su tipo: 'diagnostic', 'mbti', etc.
    """
    test = await db.tests.find_one({"type": test_type})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # Convertir ObjectId a string para que el modelo lo acepte
    test["_id"] = str(test["_id"])

    test_data = TestModel(**test)
    return test_data

@router.post("/submit")
async def submit_test(test_submit: TestSubmit, user: dict = Depends(get_current_user)):
    user_id = user["_id"]
    test_type = test_submit.test_id

    if test_type == "diagnostic":
        # Procesar respuestas: cuenta cuántas respuestas indican cada trastorno
        disorder_counts = {"anxiety": 0, "depression": 0, "adhd": 0, "stress": 0, "burnout": 0}

        for ans in test_submit.answers:
            if ans.answer in disorder_counts:
                disorder_counts[ans.answer] += 1

        # Detectar los trastornos con al menos 1 respuesta positiva
        detected = [k for k, v in disorder_counts.items() if v > 0]

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"disorders": detected},
                "$addToSet": {"completed_tests": "diagnostic"}
            }
        )

    elif test_type == "mbti":
        # Inicializar conteos
        mbti_counts = {
            "E": 0, "I": 0,
            "S": 0, "N": 0,
            "T": 0, "F": 0,
            "J": 0, "P": 0
        }

        for ans in test_submit.answers:
            if ans.answer in mbti_counts:
                mbti_counts[ans.answer] += 1

        # Calcular por ejes
        ei = "E" if mbti_counts["E"] >= mbti_counts["I"] else "I"
        sn = "S" if mbti_counts["S"] >= mbti_counts["N"] else "N"
        tf = "T" if mbti_counts["T"] >= mbti_counts["F"] else "F"
        jp = "J" if mbti_counts["J"] >= mbti_counts["P"] else "P"

        mbti_type = ei + sn + tf + jp

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"mbti_type": mbti_type},
                "$addToSet": {"completed_tests": "mbti"}
            }
        )

    else:
        raise HTTPException(status_code=400, detail="Unknown test type")

    return {"message": f"{test_type} test submitted successfully"}

@router.get("/results")
async def get_test_results(user: dict = Depends(get_current_user)):
    results = {
        "disorders": user.get("disorders", []),
        "big_five": user.get("big_five", {}),
        "mbti_type": user.get("mbti_type", None),
        "completed_tests": user.get("completed_tests", [])
    }
    return results
