from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Event
from backend.database import Base

# Подставьте путь к вашей базе данных (например, "sqlite:///./app.db")
DATABASE_URL = "sqlite:///backend/app.db"
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
            {
                "title": "Концерт симфонического оркестра",
                "description": "Исполнение произведений Чайковского и Рахманинова.",
                "date": datetime(2025, 6, 10, 19, 0, 0),
                "location": "Москва, Консерватория",
                "poster_url": "https://example.com/orchestra.jpg",
            },
            {
                "title": "Фестиваль уличной еды",
                "description": "Более 30 фуд-траков, конкурсы и живая музыка.",
                "date": datetime(2025, 7, 5, 12, 0, 0),
                "location": "Казань, Парк Горького",
                "poster_url": "https://example.com/foodfest.jpg",
            },
            {
                "title": "Мастер-класс по гончарному делу",
                "description": "Для начинающих и продолжающих. Все материалы предоставляются.",
                "date": datetime(2025, 8, 15, 14, 0, 0),
                "location": "Нижний Новгород, Арт-пространство 'Терраса'",
                "poster_url": "https://example.com/pottery.jpg",
            },
            {
                "title": "Лекция «Космос: от мечты к реальности»",
                "description": "Спикер — лётчик-космонавт, Герой России.",
                "date": datetime(2025, 9, 20, 18, 0, 0),
                "location": "Новосибирск, Планетарий",
                "poster_url": "https://example.com/space.jpg",
            },
            {
                "title": "Новогодний гала-концерт",
                "description": "Звёзды эстрады, праздничная программа, фейерверк.",
                "date": datetime(2025, 12, 31, 20, 0, 0),
                "location": "Сочи, Зимний театр",
                "poster_url": "https://example.com/newyear.jpg",
            },
            {
                "title": "Киберспортивный турнир по Dota 2",
                "description": "Призовой фонд 5 млн рублей. Регистрация команд открыта.",
                "date": datetime(2025, 11, 15, 10, 0, 0),
                "location": "Екатеринбург, КРК 'Уралец'",
                "poster_url": "https://example.com/esports.jpg",
            },
            {
                "title": "Выставка ретро-автомобилей",
                "description": "Автомобили 1950–1980 годов, интерактивные зоны.",
                "date": datetime(2026, 3, 22, 11, 0, 0),
                "location": "Краснодар, Выставочный зал",
                "poster_url": "https://example.com/retrocar.jpg",
            },
            {
                "title": "Йога-ретрит на Байкале",
                "description": "7 дней практик, медитаций и экскурсий.",
                "date": datetime(2026, 7, 1, 9, 0, 0),
                "location": "Иркутская область, озеро Байкал",
                "poster_url": "https://example.com/yoga.jpg",
            },
            {
                "title": "Фестиваль научного кино",
                "description": "Показ лучших документальных фильмов о науке, встречи с режиссёрами.",
                "date": datetime(2026, 2, 14, 12, 0, 0),
                "location": "Санкт-Петербург, киноцентр 'Дом Кино'",
                "poster_url": "https://example.com/scifi.jpg",
            },
            {
                "title": "Благотворительный забег",
                "description": "Дистанции 5 и 10 км. Все средства пойдут в фонд помощи детям.",
                "date": datetime(2025, 10, 12, 9, 0, 0),
                "location": "Москва, ВДНХ",
                "poster_url": "https://example.com/run.jpg",
            }
        ]

        for data in events_data:
            event = Event(**data)
            db.add(event)
        
        db.commit()
    finally:
        db.close()

seed_events()