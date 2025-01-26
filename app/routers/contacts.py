from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud, schemas
from typing import List
from fastapi.security import OAuth2PasswordBearer
from app.auth import decode_access_token

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload["sub"]

@router.post("/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return crud.create_contact(db=db, contact=contact, user_email=current_user)

@router.get("/", response_model=List[schemas.Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return crud.get_contacts(db=db, skip=skip, limit=limit, user_email=current_user)

@router.get("/{contact_id}", response_model=schemas.Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_contact = crud.get_contact_by_id(db=db, contact_id=contact_id, user_email=current_user)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    db_contact = crud.update_contact(db=db, contact_id=contact_id, contact=contact, user_email=current_user)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    success = crud.delete_contact(db=db, contact_id=contact_id, user_email=current_user)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@router.get("/search/", response_model=List[schemas.Contact])
def search_contacts(
    query: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return crud.search_contacts(db=db, query=query, user_email=current_user)

@router.get("/birthdays/", response_model=List[schemas.Contact])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    return crud.get_upcoming_birthdays(db=db, user_email=current_user)