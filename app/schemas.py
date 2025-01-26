from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date

# Schemas for User
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)

# Schemas for Contact
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_info: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    additional_info: Optional[str] = None

class Contact(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True)