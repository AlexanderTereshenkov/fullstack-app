from fastapi import FastAPI
from backend.routers import events
from routers import auth, user, admin
from backend.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(events.router)
app.include_router(user.router)
app.include_router(admin.router)
