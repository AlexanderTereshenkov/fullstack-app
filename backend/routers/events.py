from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, shemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User  # модель пользователя с полем role


router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", response_model=List[shemas.EventResponse])
def read_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip=skip, limit=limit)
    return events


@router.get("/{event_id}", response_model=shemas.EventResponse)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Такого события нет.")
    return db_event
