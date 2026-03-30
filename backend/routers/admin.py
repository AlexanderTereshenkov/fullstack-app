#Личный кабинет польщзователя
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, shemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User  # модель пользователя с полем role


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