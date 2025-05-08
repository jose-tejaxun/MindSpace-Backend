from fastapi import FastAPI
from app.routes import auth, user, admin

app = FastAPI(title="MindSpace API")

app.include_router(auth.router, prefix="/auth")
app.include_router(user.router, prefix="/user")
app.include_router(admin.router, prefix="/admin")

