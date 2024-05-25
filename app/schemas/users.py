from pydantic import BaseModel, EmailStr
from typing import  Optional

class UserSchema(BaseModel):

    def __getitem__(self, key):
        return getattr(self, key)
    
    id: str
    name: str
    email: EmailStr
    password: Optional[str] = None
    confirm_password: Optional[str] = None

    class Config:
        orm_mode = True
