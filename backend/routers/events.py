from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, schemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User  # модель пользователя с полем role


router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=List[schemas.EventResponse])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=schemas.EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


# Админские эндпоинты (можно вынести в admin.py)
@router.post("/", response_model=schemas.EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # зависимость, которая возвращает текущего юзера
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.create_event(db, event)


@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
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