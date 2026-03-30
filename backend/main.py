from fastapi import FastAPI
from backend.routers import events
from .routers import auth, user, admin
import backend.models
from backend.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware



#Создание всех таблиц при старте приложения
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(user.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # адрес фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
