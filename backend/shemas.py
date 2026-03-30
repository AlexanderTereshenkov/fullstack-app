from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# Базовые поля события
class EventBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    date: datetime
    location: str = Field(..., min_length=3, max_length=200)
    poster_url: Optional[str] = None


# Для создания (не нужен id, created_at, updated_at)
class EventCreate(EventBase):
    pass


# Для обновления (все поля опциональны)
class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = Field(None, min_length=3, max_length=200)
    poster_url: Optional[str] = None


# Для ответа (включаем id и метаданные)
class EventResponse(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # позволяет работать с SQLAlchemy моделями
