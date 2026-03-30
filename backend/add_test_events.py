from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Event
from backend.database import Base  # замените на правильный импорт

# Подставьте путь к вашей базе данных (например, "sqlite:///./app.db")
DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаём таблицы, если их нет
Base.metadata.create_all(bind=engine)

def seed_events():
    db = SessionLocal()
    try:
        events_data = [
            {
                "title": "Выставка современного искусства",
                "description": "Работы молодых художников.",
                "date": datetime(2025, 5, 15, 10, 0, 0),
                "location": "Санкт-Петербург, Манеж",
                "poster_url": "https://example.com/poster2.jpg",
            },
            {
                "title": "Спектакль «Вишнёвый сад»",
                "description": "Классическая постановка.",
                "date": datetime(2025, 5, 20, 18, 30, 0),
                "location": "Екатеринбург, Театр драмы",
                "poster_url": "https://example.com/poster3.jpg",
            },
        ]

        for data in events_data:
            event = Event(**data)
            db.add(event)
        
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed_events()