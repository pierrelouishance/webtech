
from fastapi import HTTPException
from app.database.database import Session
from app.models.notes import Notes
from uuid import uuid4
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from app.models.users import User
from werkzeug.security import generate_password_hash

from app.schemas.notes import NoteSchema
from app.schemas.users import UserSchema

def get_db():
    return Session()

# def get_all_books():
#     with get_db() as db:
#         return db.query(Note).all()
    
# def get_books_with_owners():
#     with get_db() as db:
#         return db.query(Note).options(joinedload(Note.owner)).all()