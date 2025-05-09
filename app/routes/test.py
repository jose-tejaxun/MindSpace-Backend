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
    Obtiene las preguntas del test según su tipo: 'diagnostic' o 'personality'
    """
    test = await db.tests.find_one({"type": test_type})
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    test_data = TestModel(**test)
    return test_data

@router.post("/submit")
async def submit_test(test_submit: TestSubmit, user: dict = Depends(get_current_user)):
    user_id = user["_id"]
    test_type = test_submit.test_id

    if test_type == "diagnostic":
        # Procesar respuestas: cuenta cuántas respuestas indican cada trastorno
        disorder_counts = {"anxiety": 0, "depression": 0, "adhd": 0}

        for ans in test_submit.answers:
            # Aquí se asume que la respuesta directa es el nombre del trastorno
            if ans.answer in disorder_counts:
                disorder_counts[ans.answer] += 1

        # Determinar los trastornos detectados (al menos 1 respuesta relacionada)
        detected = [k for k, v in disorder_counts.items() if v > 0]

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"disorders": detected},
                "$addToSet": {"completed_tests": "diagnostic"}
            }
        )

    elif test_type == "personality":
        # Procesar respuestas para Big Five (simplificado)
        big_five_result = {
            "openness": 0,
            "conscientiousness": 0,
            "extraversion": 0,
            "agreeableness": 0,
            "neuroticism": 0
        }

        for ans in test_submit.answers:
            # Se asume que question_id es el rasgo y answer es un número
            if ans.question_id in big_five_result:
                big_five_result[ans.question_id] += int(ans.answer)

        # Normalizar a máximo 100 (opcional, depende de tu escala)
        for trait in big_five_result:
            big_five_result[trait] = min(100, big_five_result[trait])

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {"big_five": big_five_result},
                "$addToSet": {"completed_tests": "personality"}
            }
        )

    else:
        raise HTTPException(status_code=400, detail="Unknown test type")

    return {"message": f"{test_type} test submitted successfully"}
