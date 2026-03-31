from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import User
from backend.database import Base
from backend.utils.security import verify_password, get_password_hash 

# Подставьте путь к вашей базе данных (например, "sqlite:///./app.db")
DATABASE_URL = "sqlite:///backend/app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём таблицы, если их нет
Base.metadata.create_all(bind=engine)

def seed_users():
    db = SessionLocal()
    try:
        events_data = [
            {
                "email":"admin1@example.com",
                "hashed_password": get_password_hash("1234567"),
                "role":"admin"
            },
            {
                "email":"admin2@example.com",
                "hashed_password": get_password_hash("1234567"),
                "role":"admin"
            },
        ]

        for data in events_data:
            event = User(**data)
            db.add(event)
        
        db.commit()
    finally:
        db.close()

seed_users()
