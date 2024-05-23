from pydantic import BaseModel
from typing import Optional
from datetime import date

# Import du type User depuis le fichier types.py
from app.schemas.types import User

class NoteBase(BaseModel):
    text: str
    category: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    text: Optional[str] = None
    category: Optional[str] = None

class Note(NoteBase):
    id: str
    owner_id: str

    class Config:
        orm_mode = True

class NoteWithOwner(Note):
    owner: 'User'

    class Config:
        orm_mode = True
