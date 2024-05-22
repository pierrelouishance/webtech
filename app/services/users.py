from uuid import uuid4
from fastapi import HTTPException
from app.database.database import Session
from app.models.users import User 
from werkzeug.security import generate_password_hash,  check_password_hash

from app.schemas.users import UserSchema

def get_db():
    return Session()

def get_all_users():
    with get_db() as db:
        return db.query(User).all()
    
def get_user_by_email(email: str):
    with get_db() as db:
        return db.query(User).filter(User.email == email).first()

def get_user_by_id(id: str):
    with get_db() as db:
        return db.query(User).filter(User.id == id).first()
