from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.services.speech_service import audio_to_text, text_to_audio
from app.services.dependencies import get_current_user
from app.database import db
from datetime import datetime

router = APIRouter()

@router.post("/voice")
async def voice_chat(
    audio: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    try:
        # Convertir audio a texto
        user_input = audio_to_text(audio.file)

        # Lógica de respuesta simple (puedes conectar GPT luego)
        if "triste" in user_input.lower():
            bot_response = "Lamento que te sientas así. ¿Quieres hablar de ello?"
        else:
            bot_response = "Gracias por compartirlo. Estoy aquí para ayudarte."

        # Mensajes
        user_msg = {
            "sender": "user",
            "message": user_input,
            "timestamp": datetime.utcnow()
        }
        bot_msg = {
            "sender": "bot",
            "message": bot_response,
            "timestamp": datetime.utcnow()
        }

        # Guardar conversación en la colección `chat`
        existing_session = db.chat.find_one({"user_id": str(user["_id"])})

        if existing_session:
            db.chat.update_one(
                {"user_id": str(user["_id"])},
                {"$push": {"messages": {"$each": [user_msg, bot_msg]}}}
            )
        else:
            db.chat.insert_one({
                "user_id": str(user["_id"]),
                "messages": [user_msg, bot_msg]
            })

        # Convertir respuesta a audio
        audio_output = text_to_audio(bot_response)

        return {
            "text": bot_response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_chat_history(user: dict = Depends(get_current_user)):
    session = db.chat.find_one({"user_id": str(user["_id"])})
    if not session:
        return {"messages": []}
    return {"messages": session["messages"]}
