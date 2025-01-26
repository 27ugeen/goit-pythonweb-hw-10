from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db, verify_password
from app.auth import create_access_token, decode_access_token
from app.email_utils import send_verification_email
from app.models import User
from app import crud, schemas

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/token", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Новий маршрут для реєстрації користувачів
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    new_user = crud.create_user(db, user)
    
    # Надсилання верифікаційного email у фоновому режимі
    background_tasks.add_task(send_verification_email, new_user.email)
    return new_user

@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token does not contain an email")

    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.is_verified:
        return {"message": "Email is already verified."}

    user.is_verified = True
    db.add(user)
    db.commit()

    return {"message": "Email successfully verified."}