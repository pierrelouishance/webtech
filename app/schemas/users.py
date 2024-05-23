from pydantic import BaseModel, EmailStr
from typing import List, Optional

# Import du type Note depuis le fichier types.py
from app.schemas.types import Note

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class User(UserBase):
    id: str

    class Config:
        orm_mode = True

class UserWithNotes(User):
    notes: List['Note'] = []

    class Config:
        orm_mode = True
