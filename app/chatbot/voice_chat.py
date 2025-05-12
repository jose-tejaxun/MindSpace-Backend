from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
import tempfile
import shutil
import whisper
import openai
import os
from gtts import gTTS
from app.schemas.chat_schema import VoiceChatResponse

router = APIRouter()

# Leer la clave de API de OpenAI desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@router.post("/voice-chat", response_model=VoiceChatResponse | None)
async def voice_chat(
    audio: UploadFile = File(...),
    return_type: str = Query("audio", enum=["audio", "json"])
):
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            shutil.copyfileobj(audio.file, temp_audio)
            temp_audio_path = temp_audio.name

        # Transcribir con Whisper
        model = whisper.load_model("base")
        result = model.transcribe(temp_audio_path)
        transcript = result["text"]

        # Obtener respuesta de GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": transcript}]
        )
        response_text = response["choices"][0]["message"]["content"]

        # Convertir respuesta a voz
        audio_response_path = temp_audio_path.replace(".wav", "_response.mp3")
        tts = gTTS(response_text, lang="es")
        tts.save(audio_response_path)

        # Elegir tipo de respuesta según parámetro
        if return_type == "json":
            return VoiceChatResponse(question=transcript, answer=response_text)

        return FileResponse(audio_response_path, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
