from sqlalchemy.orm import Session
from app.models import Contact, User
from app.schemas import ContactCreate, ContactUpdate, UserCreate
from typing import List, Optional
from datetime import date, timedelta
from bcrypt import hashpw, gensalt


# Отримати користувача за email
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


# Створити нового користувача
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hashpw(user.password.encode("utf-8"), gensalt()).decode("utf-8")
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Створити новий контакт, прив'язаний до користувача
def create_contact(db: Session, contact: ContactCreate, user_email: str) -> Contact:
    user = get_user_by_email(db, user_email)
    if not user:
        raise ValueError("User not found")
    db_contact = Contact(**contact.model_dump(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Отримати всі контакти для користувача
def get_contacts(db: Session, user_email: str, skip: int = 0, limit: int = 10) -> List[Contact]:
    user = get_user_by_email(db, user_email)
    if not user:
        return []
    return db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()


# Отримати контакт за ID (перевірка належності користувачу)
def get_contact_by_id(db: Session, contact_id: int, user_email: str) -> Optional[Contact]:
    user = get_user_by_email(db, user_email)
    if not user:
        return None
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()


# Оновити контакт
def update_contact(db: Session, contact_id: int, contact: ContactUpdate, user_email: str) -> Optional[Contact]:
    user = get_user_by_email(db, user_email)
    if not user:
        return None
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if not db_contact:
        return None
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


# Видалити контакт
def delete_contact(db: Session, contact_id: int, user_email: str) -> bool:
    user = get_user_by_email(db, user_email)
    if not user:
        return False
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user.id).first()
    if not db_contact:
        return False
    db.delete(db_contact)
    db.commit()
    return True


# Пошук контактів користувача
def search_contacts(db: Session, query: str, user_email: str) -> List[Contact]:
    user = get_user_by_email(db, user_email)
    if not user:
        return []
    return db.query(Contact).filter(
        Contact.user_id == user.id,
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


# Отримати дні народження на найближчий тиждень для користувача
def get_upcoming_birthdays(db: Session, user_email: str) -> List[Contact]:
    user = get_user_by_email(db, user_email)
    if not user:
        return []
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(
        Contact.user_id == user.id,
        Contact.birthday >= today,
        Contact.birthday <= next_week
    ).all()