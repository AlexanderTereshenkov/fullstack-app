from fastapi import FastAPI
from backend.routers import events
from .routers import auth, user, admin
import backend.models
from backend.database import engine, Base

#Создание всех таблиц при старте приложения
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(user.router)
app.include_router(admin.router)

