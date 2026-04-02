#Личный кабинет польщзователя
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from backend import crud, shemas
from backend.dependencies import get_db, get_current_user  # предположим, что есть такие зависимости
from backend.models import User  # модель пользователя с полем role
from datetime import datetime
from backend.service.ocr_llm_service import extract_event_data_from_image


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/me")
def get_admin_events(current_user: User = Depends(get_current_user),
                     db: Session = Depends(get_db),):
    return crud.get_admin_events(db, current_user.id)


@router.put("/update_event/{event_id}", response_model=shemas.EventResponse)
def update_event(
    event_id: int,
    event_update: shemas.EventUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав.")
    event_creator_id = crud.get_event(db, event_id).admin_id
    if not event_creator_id or current_user.id != event_creator_id:
        raise HTTPException(status_code=403, detail="Мы не владеем событием.")
    
    date_str = event_update.date
    time_str = event_update.time or "00:00"
    print("UPDATE TIME", date_str, time_str)
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильный формат даты/времени")

    event_dict = event_update.dict(exclude={"date", "time"})
    event_dict["date"] = dt
    db_event = crud.update_event(db, event_id, event_dict)
    if not db_event:
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    return db_event


@router.delete("/delete_event/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав.")
    if not crud.delete_event(db, event_id):
        raise HTTPException(status_code=404, detail="Событие не найдено.")
    

@router.post("/add_event", response_model=shemas.EventResponse)
def add_event(
    event_data: shemas.EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав.")

    # Объединяем дату и время в один datetime
    date_str = event_data.date
    time_str = event_data.time or "00:00"
    try:
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильный формат даты/времени")

    # Подготавливаем данные для создания события
    event_dict = event_data.dict(exclude={"date", "time"})
    event_dict["date"] = dt
    # Если нужно сохранить poster_url, добавьте его из event_dict (он уже там)
    event_dict["admin_id"] = current_user.id  # запоминаем, кто создал
    db_event = crud.create_event(db, event_dict)
    return db_event


@router.get("/check_event/{event_id}", response_model=shemas.TicketAdminRespone)
def check_event_admin(event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    event_creator_id = crud.get_event(db, event_id).admin_id
    return {"admin_id":current_user.id, "event_creator_id":event_creator_id}


@router.post("/ocr")
async def admin_ocr(file: UploadFile = File(...),
              current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Недостаточно прав.")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Файл должен быть изображением")

    image_bytes = await file.read()

    try:
        parsed_data = extract_event_data_from_image(image_bytes)
    except Exception as e:
        raise HTTPException(500, f"Ошибка распознавания: {str(e)}")

    return parsed_data

