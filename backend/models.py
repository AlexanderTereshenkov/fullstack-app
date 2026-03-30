from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # "admin" или "user"
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    tickets = relationship("Ticket", back_populates="user")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    poster_url = Column(String)  # ссылка на афишу
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), 
                        onupdate=datetime.now(timezone.utc))

    tickets = relationship("Ticket", back_populates="event")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    purchased_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="tickets")
    event = relationship("Event", back_populates="tickets")