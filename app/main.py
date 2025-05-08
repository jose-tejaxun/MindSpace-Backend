from fastapi import FastAPI
from app.routes import auth_routes, user_routes  # Agregar más después

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")

@app.get("/")
def root():
    return {"message": "Bienvenido a HealthyMind API"}
