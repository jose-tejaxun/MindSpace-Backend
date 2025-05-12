import speech_recognition as sr
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment

def audio_to_text(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = recognizer.record(source)
    return recognizer.recognize_google(audio_data, language='es-ES')

def text_to_audio(text):
    tts = gTTS(text, lang='es')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio = AudioSegment.from_file(mp3_fp, format="mp3")
    output = BytesIO()
    audio.export(output, format="wav")
    output.seek(0)
    return output
