from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, user, admin, test, chatbot

app = FastAPI()

origins = [
    "http://localhost:3000",  # para pruebas locales
    "https://mind-space-frontend.vercel.app"  # tu frontend en Vercel
]

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
app.include_router(test.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
