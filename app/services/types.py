from uuid import uuid4
from fastapi import HTTPException
from app.database.database import Session
from app.models.notes import Note
from app.models.user_notes import UserNote
from app.models.users import User 
from app.schemas.types import NoteShareSchema

def get_db():
    return Session()

def share_note_with_user(note_share_data: NoteShareSchema):
    with get_db() as db:
        note_share_entity = UserNote(
            user_id=note_share_data.user_id,
            note_id=note_share_data.note_id
        )
        db.add(note_share_entity)
        db.commit()

def get_shared_notes(user_id: str):
    with get_db() as db:
        return db.query(Note).join(UserNote, Note.id == UserNote.note_id).filter(UserNote.user_id == user_id).all()