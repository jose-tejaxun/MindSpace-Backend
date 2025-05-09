import pymongo

# Conexión MongoDB local
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mindspace"]
tests_collection = db["tests"]

# Limpiar colección antes (opcional, cuidado)
tests_collection.delete_many({})

# ---------- TEST DIAGNÓSTICO (AMPLIADO) ----------
diagnostic_questions = []
for i in range(1, 51):
    if i <= 10:
        category = "anxiety"
        text = f"Pregunta {i}: ¿Experimentas síntomas de ansiedad como preocupación constante?"
    elif i <= 20:
        category = "depression"
        text = f"Pregunta {i}: ¿Experimentas síntomas de depresión como pérdida de interés?"
    elif i <= 30:
        category = "adhd"
        text = f"Pregunta {i}: ¿Tienes síntomas de TDAH como dificultad para concentrarte?"
    elif i <= 40:
        category = "stress"
        text = f"Pregunta {i}: ¿Te sientes estresado frecuentemente?"
    else:
        category = "burnout"
        text = f"Pregunta {i}: ¿Te sientes agotado o quemado por el trabajo?"

    diagnostic_questions.append({
        "id": f"q{i}",
        "text": text,
        "options": ["yes", "no"],
        "correct_answer": category
    })

diagnostic_test = {
    "type": "diagnostic",
    "title": "Test de diagnóstico de salud mental (extendido)",
    "description": "Responde estas 50 preguntas para detectar posibles trastornos como ansiedad, depresión, TDAH, estrés o burnout.",
    "questions": diagnostic_questions
}

# ---------- TEST MBTI (AMPLIADO) ----------
mbti_questions = []
# Repartir 50 preguntas entre los 4 ejes
for i in range(1, 13):
    mbti_questions.append({
        "id": "ei",
        "text": f"Pregunta {i}: Prefieres actividades en grupo que estar solo.",
        "options": ["E", "I"]
    })
for i in range(13, 25):
    mbti_questions.append({
        "id": "sn",
        "text": f"Pregunta {i}: Confías más en hechos concretos que en intuiciones.",
        "options": ["S", "N"]
    })
for i in range(25, 37):
    mbti_questions.append({
        "id": "tf",
        "text": f"Pregunta {i}: Tomas decisiones más con lógica que con sentimientos.",
        "options": ["T", "F"]
    })
for i in range(37, 51):
    mbti_questions.append({
        "id": "jp",
        "text": f"Pregunta {i}: Prefieres tener un plan fijo que ser espontáneo.",
        "options": ["J", "P"]
    })

mbti_test = {
    "type": "mbti",
    "title": "Test de Personalidad MBTI (extendido)",
    "description": "Descubre tu tipo MBTI respondiendo estas 50 preguntas.",
    "questions": mbti_questions
}

# ---------- INSERTAR EN MONGODB ----------
tests_collection.insert_many([diagnostic_test, mbti_test])

print("✅ Tests extendidos insertados exitosamente en MongoDB")
