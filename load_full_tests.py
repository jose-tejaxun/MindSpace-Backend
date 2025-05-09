import pymongo
import os
from dotenv import load_dotenv

# Cargar variables del entorno
load_dotenv()

# Leer URL desde .env
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise Exception("Falta la variable MONGO_URL en el archivo .env")

# Conexión pymongo (sincrónica)
client = pymongo.MongoClient(MONGO_URL)
db = client["mindspace"]
tests_collection = db["tests"]

# Limpiar colección antes (opcional, cuidado)
tests_collection.delete_many({})

# ---------- TEST DIAGNÓSTICO ----------
diagnostic_questions = []
for i in range(1, 51):
    if i <= 10:
        category = "anxiety"
        text = f"Pregunta {i}: ¿Te sientes nervioso o preocupado frecuentemente?"
    elif i <= 20:
        category = "depression"
        text = f"Pregunta {i}: ¿Te sientes triste o sin energía la mayoría del tiempo?"
    elif i <= 30:
        category = "adhd"
        text = f"Pregunta {i}: ¿Te cuesta concentrarte incluso en tareas simples?"
    elif i <= 40:
        category = "stress"
        text = f"Pregunta {i}: ¿Sientes que tu carga diaria te sobrepasa?"
    else:
        category = "burnout"
        text = f"Pregunta {i}: ¿Te sientes agotado emocionalmente por el trabajo o estudio?"

    diagnostic_questions.append({
        "id": f"q{i}",
        "text": text,
        "options": ["yes", "no"],
        "correct_answer": category
    })

diagnostic_test = {
    "type": "diagnostic",
    "title": "Test de diagnóstico de salud mental (extendido)",
    "description": "Responde estas 50 preguntas para detectar posibles síntomas de ansiedad, depresión, TDAH, estrés o burnout.",
    "questions": diagnostic_questions
}

# ---------- TEST MBTI (50 preguntas reales y variadas) ----------
mbti_questions = []

# E/I (Extroversión / Introversión)
ei_questions = [
    ("En las fiestas, prefiero socializar con muchos", "E", "Prefiero hablar con unas pocas personas", "I"),
    ("Me energiza estar rodeado de gente", "E", "Prefiero momentos de soledad para recargarme", "I"),
    ("Me siento cómodo hablando en público", "E", "Prefiero escuchar más que hablar", "I"),
    ("Me resulta fácil iniciar conversaciones", "E", "Prefiero esperar a que otros se acerquen", "I"),
    ("Disfruto de actividades grupales", "E", "Prefiero actividades en solitario", "I"),
    ("Me distraigo menos cuando trabajo solo", "I", "Trabajo mejor rodeado de otros", "E"),
    ("Siento que la soledad me drena", "E", "Encuentro paz en la soledad", "I"),
    ("Prefiero ambientes ruidosos", "E", "Prefiero ambientes tranquilos", "I"),
    ("Suelo actuar antes de reflexionar", "E", "Suelo pensar antes de actuar", "I"),
    ("Me motiva la interacción social", "E", "Me motiva el tiempo personal", "I"),
    ("En reuniones, hablo mucho", "E", "En reuniones, escucho más", "I"),
    ("Prefiero compartir mis pensamientos abiertamente", "E", "Prefiero reflexionar antes de compartir", "I"),
]

# S/N (Sensación / Intuición)
sn_questions = [
    ("Confío en hechos comprobables", "S", "Confío en ideas y posibilidades", "N"),
    ("Me concentro en detalles prácticos", "S", "Me concentro en el panorama general", "N"),
    ("Prefiero instrucciones claras y paso a paso", "S", "Prefiero explorar mi propio enfoque", "N"),
    ("Me interesa lo que es real y concreto", "S", "Me interesa lo imaginativo y teórico", "N"),
    ("Aprendo mejor con ejemplos reales", "S", "Aprendo mejor explorando ideas", "N"),
    ("Soy cuidadoso con los detalles", "S", "Prefiero saltar a las grandes ideas", "N"),
    ("Me guío por experiencias pasadas", "S", "Me guío por lo que podría ser", "N"),
    ("Me gusta seguir rutinas conocidas", "S", "Me gusta probar nuevos enfoques", "N"),
    ("Prefiero datos tangibles", "S", "Prefiero patrones y conexiones", "N"),
    ("Valoro lo comprobable", "S", "Valoro lo innovador", "N"),
    ("Me centro en el presente", "S", "Me centro en posibilidades futuras", "N"),
    ("Trabajo mejor con certezas", "S", "Trabajo bien con ambigüedades", "N"),
]

# T/F (Pensamiento / Sentimiento)
tf_questions = [
    ("Tomo decisiones con lógica", "T", "Tomo decisiones según emociones", "F"),
    ("Valoro la justicia", "T", "Valoro la empatía", "F"),
    ("Creo en decir la verdad directa", "T", "Creo en proteger sentimientos", "F"),
    ("Resuelvo conflictos con objetividad", "T", "Resuelvo conflictos considerando emociones", "F"),
    ("Me motivan los logros", "T", "Me motivan las relaciones", "F"),
    ("Analizo problemas racionalmente", "T", "Considero cómo afecta a otros", "F"),
    ("Prefiero criticar para mejorar", "T", "Prefiero alentar para apoyar", "F"),
    ("Evito dejarme llevar por emociones", "T", "Sigo lo que me hace sentir bien", "F"),
    ("Busco eficiencia", "T", "Busco armonía", "F"),
    ("Me gusta debatir", "T", "Prefiero evitar confrontaciones", "F"),
    ("Valoro principios", "T", "Valoro la compasión", "F"),
    ("Prefiero ser justo que compasivo", "T", "Prefiero ser compasivo que justo", "F"),
]

# J/P (Juicio / Percepción)
jp_questions = [
    ("Me gusta tener planes detallados", "J", "Prefiero mantenerme flexible", "P"),
    ("Prefiero cerrar asuntos rápidamente", "J", "Prefiero mantener opciones abiertas", "P"),
    ("Trabajo mejor con calendarios y listas", "J", "Trabajo mejor improvisando", "P"),
    ("Me molesta la incertidumbre", "J", "Encuentro emocionante la incertidumbre", "P"),
    ("Prefiero horarios fijos", "J", "Prefiero fluir con lo que surja", "P"),
    ("Sigo reglas establecidas", "J", "Prefiero adaptarlas según lo necesite", "P"),
    ("Disfruto completando tareas", "J", "Disfruto comenzando nuevas tareas", "P"),
    ("Me gusta la estructura", "J", "Me gusta la espontaneidad", "P"),
    ("Planeo antes de actuar", "J", "Actúo según lo que surja", "P"),
    ("Prefiero organizar mi día", "J", "Prefiero ver qué pasa", "P"),
    ("Me siento incómodo con cambios repentinos", "J", "Me adapto rápido a cambios", "P"),
    ("Me gusta terminar proyectos antes de tiempo", "J", "Me gusta trabajar cerca de la fecha límite", "P"),
]

for i, (text, label1, text2, label2) in enumerate(ei_questions + sn_questions + tf_questions + jp_questions, start=1):
    # Determinar el eje según las etiquetas
    if label1 in ["E", "I"]:
        axis = "ei"
    elif label1 in ["S", "N"]:
        axis = "sn"
    elif label1 in ["T", "F"]:
        axis = "tf"
    else:
        axis = "jp"

    mbti_questions.append({
        "id": axis,
        "text": f"Pregunta {i}: {text} o {text2}?",
        "options": [
            {"label": text, "value": label1},
            {"label": text2, "value": label2}
        ]
    })

mbti_test = {
    "type": "mbti",
    "title": "Test de Personalidad MBTI (completo)",
    "description": "Responde estas 50 preguntas para descubrir tu tipo de personalidad MBTI.",
    "questions": mbti_questions
}

# ---------- INSERTAR EN MONGODB ----------
tests_collection.insert_many([diagnostic_test, mbti_test])

print("✅ Tests completos insertados exitosamente en MongoDB")
