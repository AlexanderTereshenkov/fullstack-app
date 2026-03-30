from sqlalchemy.orm import Session
from backend import models, schemas


# ---- События ----
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def update_event(db: Session, event_id: int, event_update: schemas.EventUpdate):
    db_event = get_event(db, event_id)
    if not db_event:
        return None
    update_data = event_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_event, field, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = get_event(db, event_id)
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return True


# ---- Пользователи ----
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        role="user"  # по умолчанию
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

