from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from backend import crud, shemas, dependencies
from backend.database import get_db
from backend.utils.security import verify_password, get_password_hash  # напишем ниже


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=shemas.UserResponse)
def register(user: shemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = crud.create_user(db, user, hashed_password)
    return db_user


@router.post("/login", response_model=shemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = dependencies.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    # На стороне сервера обычно ничего не делается, клиент просто удаляет токен
    return {"message": "Logged out"}

