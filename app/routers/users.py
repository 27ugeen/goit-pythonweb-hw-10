from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import get_user_by_email, create_user

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists.")
    return create_user(db, user)