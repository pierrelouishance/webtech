from pydantic import BaseModel
from typing import Optional
from datetime import date

class NoteSchema(BaseModel):
    id: str
    text: Optional[str] = None
    category: Optional[str] = None
    owner_id: str

    class Config:
        orm_mode = True
