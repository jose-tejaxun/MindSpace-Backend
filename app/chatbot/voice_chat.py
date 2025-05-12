from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import tempfile
import shutil
import whisper
import openai
import os
from gtts import gTTS

router = APIRouter()

# Leer la clave de API de OpenAI desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@router.post("/voice-chat")
async def voice_chat(audio: UploadFile = File(...)):
    try:
        # Guardar el archivo temporalmente
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            shutil.copyfileobj(audio.file, temp_audio)
            temp_audio_path = temp_audio.name

        # Transcribir con Whisper
        model = whisper.load_model("base")  # Puedes usar tiny/small/medium/large
        result = model.transcribe(temp_audio_path)
        transcript = result["text"]

        # Obtener respuesta de GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": transcript}]
        )
        response_text = response["choices"][0]["message"]["content"]

        # Convertir respuesta a voz (TTS)
        audio_response_path = temp_audio_path.replace(".wav", "_response.mp3")
        tts = gTTS(response_text, lang="es")
        tts.save(audio_response_path)

        # Retornar el archivo de audio como respuesta
        return FileResponse(audio_response_path, media_type="audio/mpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

