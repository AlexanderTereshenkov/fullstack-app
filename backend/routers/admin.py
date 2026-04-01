#Личный кабинет польщзователя
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, shemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User  # модель пользователя с полем role
from datetime import datetime


router = APIRouter(prefix="/admin", tags=["admin"])


@router.put("/{event_id}", response_model=shemas.EventResponse)
def update_event(
    event_id: int,
    event_update: shemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    db_event = crud.update_event(db, event_id, event_update)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    if not crud.delete_event(db, event_id):
        raise HTTPException(status_code=404, detail="Event not found")
    

@router.post("/add_event", response_model=shemas.EventResponse)
def add_event(
    event_data: shemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Объединяем дату и время в один datetime
    date_str = event_data.date
    time_str = event_data.time or "00:00"
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date or time format")

    # Подготавливаем данные для создания события
    event_dict = event_data.dict(exclude={"date", "time"})
    event_dict["date"] = dt
    # Если нужно сохранить poster_url, добавьте его из event_dict (он уже там)
    event_dict["admin_id"] = current_user.id  # запоминаем, кто создал
    db_event = crud.create_event(db, event_dict)
    return db_event

