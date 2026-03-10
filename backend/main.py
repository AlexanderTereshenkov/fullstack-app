from fastapi import FastAPI
from .routers import auth, tickets, user, admin

app = FastAPI()
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(user.router)
app.include_router(admin.router)
