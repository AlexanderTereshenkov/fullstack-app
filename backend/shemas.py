from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# === Пользователи ===
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=72)

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


# === Токен ===
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: str = "user"

class TokenData(BaseModel):
    email: str


# === События ===
class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    date: datetime
    location: str = Field(..., min_length=3, max_length=200)
    poster_url: Optional[str] = None

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = Field(None, min_length=3, max_length=200)
    poster_url: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# === Билеты ===
class TicketResponse(BaseModel):
    id: int
    event_id: int
    purchased_at: datetime
    qr_code: str

    class Config:
        orm_mode = True
