#Личный кабинет польщзователя
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from backend import crud, shemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User, Ticket  # модель пользователя с полем role


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=shemas.UserResponse)
def get_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/add_ticket/{ticket_id}")
def add_ticket(ticket_id:int, 
               current_user: User = Depends(get_current_user), 
               db: Session = Depends(get_db)):

    event = crud.get_event(db, ticket_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_ticket = db.query(Ticket).filter(
        Ticket.user_id == current_user.id,
        Ticket.event_id == ticket_id
    ).first()
    if existing_ticket:
        raise HTTPException(status_code=400, detail="Ticket already purchased")

    # 3. Создаём билет
    new_ticket = Ticket(
        user_id=current_user.id,
        event_id=ticket_id,
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "id": new_ticket.id,
        "user_id": new_ticket.user_id,
        "event_id": new_ticket.event_id,
        "purchased_at": new_ticket.purchased_at
    }


@router.get('/me/tickets')
def get_user_tickets(current_user: User = Depends(get_current_user), 
                     db: Session = Depends(get_db)):
    return crud.get_user_events(db, current_user.id)

@router.post("/delete_ticket/{ticket_id}")
def delete_ticket(ticket_id:int):
    '''
    Удаляем билет из БД юзера
    '''
    return {"result":"delete ticket"}


@router.post("/qr")
def create_qr():
    '''
    Создаем QR на сервере возвращаем пользователю
    '''
    return {"result":"QR IMAGE"}
