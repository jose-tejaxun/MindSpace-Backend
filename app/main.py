from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from app.routes import auth, user, admin, test, chatbot
=======
from app.routes import auth, user, admin
from app.chatbot import voice_chat
>>>>>>> bc2679398a0ec671be89d14be920cd1d7bf79a1d

app = FastAPI()

origins = [
    "http://localhost:3000",  # para pruebas locales
    "https://mind-space-frontend.vercel.app"  # tu frontend en Vercel
]

app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(admin.router, prefix="/admin")
<<<<<<< HEAD
app.include_router(test.router)


=======
app.include_router(voice_chat.router, prefix="/chatbot")
>>>>>>> bc2679398a0ec671be89d14be920cd1d7bf79a1d
