
from fastapi import HTTPException
from app.database.database import Session
from app.models.notes import Note
from uuid import uuid4
from sqlalchemy.orm import joinedload
from app.schemas.notes import NoteSchema
from app.schemas.users import UserSchema



def get_db():
    return Session()

def get_all_note():
    with get_db() as db:
        return db.query(Note).all()

def get_user_notes(owner_id: str):
    with get_db() as db:
        return db.query(Note).filter(Note.owner_id == owner_id).all()

def get_notes_with_owners():
    with get_db() as db:
        return db.query(Note).options(joinedload(Note.owner)).all()


def save_note(new_notes: NoteSchema, user : UserSchema):
    with get_db() as db:

        new_notes_entity = Note(
            id = str(uuid4()),
            text = new_notes.text,
            category  = new_notes.category,
            owner_id = user.id,
        )
        db.add(new_notes_entity)
        db.commit()

def delete_note(note_id: str, owner_id: str):
    with get_db() as db:
        note = db.query(Note).filter(Note.id == note_id, Note.owner_id == owner_id).first()
        if note:
            db.delete(note)
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Note not found")

def get_note_by_id(note_id: str, owner_id: str):
    with get_db() as db:
        note = db.query(Note).filter(Note.id == note_id, Note.owner_id == owner_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    
def update_note(note_id: str, owner_id: str, new_text: str, new_category: str):
    with get_db() as db:
        note = db.query(Note).filter(Note.id == note_id, Note.owner_id == owner_id).first()
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        note.text = new_text
        note.category = new_category
        db.commit()
        return note