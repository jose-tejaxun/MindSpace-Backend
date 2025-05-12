import pymongo

# Configura tu conexión (ajusta si usas usuario/contraseña)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mindspace"]

# Colección de tests
tests_collection = db["tests"]

# Limpia los tests existentes (opcional, cuidado)
tests_collection.delete_many({})

# Test diagnóstico (más completo)
diagnostic_test = {
    "type": "diagnostic",
    "title": "Test de diagnóstico de salud mental",
    "description": "Responde estas preguntas para detectar posibles trastornos como ansiedad, depresión o TDAH.",
    "questions": [
        {
            "id": "q1",
            "text": "¿Te sientes ansioso con frecuencia?",
            "options": ["yes", "no"],
            "correct_answer": "anxiety"
        },
        {
            "id": "q2",
            "text": "¿Tienes dificultad para dormir por preocupaciones constantes?",
            "options": ["yes", "no"],
            "correct_answer": "anxiety"
        },
        {
            "id": "q3",
            "text": "¿Sientes tristeza persistente o falta de interés en actividades?",
            "options": ["yes", "no"],
            "correct_answer": "depression"
        },
        {
            "id": "q4",
            "text": "¿Te sientes fatigado o sin energía casi todos los días?",
            "options": ["yes", "no"],
            "correct_answer": "depression"
        },
        {
            "id": "q5",
            "text": "¿Tienes dificultades para concentrarte o mantener la atención?",
            "options": ["yes", "no"],
            "correct_answer": "adhd"
        },
        {
            "id": "q6",
            "text": "¿Actúas impulsivamente o tienes problemas para quedarte quieto?",
            "options": ["yes", "no"],
            "correct_answer": "adhd"
        }
    ]
}

# Test personalidad Big Five (10 preguntas, 2 por rasgo)
personality_test = {
    "type": "personality",
    "title": "Test de personalidad Big Five",
    "description": "Responde estas preguntas para medir tus rasgos de personalidad.",
    "questions": [
        {
            "id": "openness",
            "text": "Disfruto explorar nuevas ideas y experiencias.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "openness",
            "text": "Tengo una gran imaginación.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "conscientiousness",
            "text": "Soy organizado y responsable en mi vida diaria.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "conscientiousness",
            "text": "Planifico cuidadosamente antes de actuar.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "extraversion",
            "text": "Me siento energizado al estar rodeado de otras personas.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "extraversion",
            "text": "Disfruto ser el centro de atención.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "agreeableness",
            "text": "Me preocupo por el bienestar de los demás.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "agreeableness",
            "text": "Soy considerado y cooperativo.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "neuroticism",
            "text": "Siento ansiedad o estrés con frecuencia.",
            "options": ["1", "2", "3", "4", "5"]
        },
        {
            "id": "neuroticism",
            "text": "A menudo me siento inseguro o preocupado.",
            "options": ["1", "2", "3", "4", "5"]
        }
    ]
}

# Inserta los tests
tests_collection.insert_many([diagnostic_test, personality_test])

print("✅ Tests insertados exitosamente en MongoDB")
