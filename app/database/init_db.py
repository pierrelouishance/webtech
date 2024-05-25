from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.users import User
from app.models.notes import Note
from app.models.user_notes import UserNote
from app.database.database import Session
from werkzeug.security import generate_password_hash

def init_db():
    db = Session()

    try:
        # Vérification et création des utilisateurs de démonstration
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                id=str(uuid4()),
                email="admin@example.com",
                name="Admin",
                password=generate_password_hash("admin"),
                confirm_password=generate_password_hash("admin"),
            )
            db.add(admin)

        user1 = db.query(User).filter(User.email == "user1@example.com").first()
        if not user1:
            user1 = User(
                id=str(uuid4()),
                email="user1@example.com",
                name="User One",
                password=generate_password_hash("password1"),
                confirm_password=generate_password_hash("password1"),
            )
            db.add(user1)

        user2 = db.query(User).filter(User.email == "user2@example.com").first()
        if not user2:
            user2 = User(
                id=str(uuid4()),
                email="user2@example.com",
                name="User Two",
                password=generate_password_hash("password2"),
                confirm_password=generate_password_hash("password2"),
            )
            db.add(user2)

        db.commit()

        # Création des notes de démonstration
        note1 = db.query(Note).join(User).filter(Note.text == "Note 1 text", User.email == "user1@example.com").first()
        if not note1:
            note1 = Note(
                id=str(uuid4()),
                text="Note 1 text",
                category="Category A",
                owner_id=user1.id,
            )
            db.add(note1)

        note2 = db.query(Note).join(User).filter(Note.text == "Note 2 text", User.email == "user1@example.com").first()
        if not note2:
            note2 = Note(
                id=str(uuid4()),
                text="Note 2 text",
                category="Category B",
                owner_id=user1.id,
            )
            db.add(note2)

        note3 = db.query(Note).join(User).filter(Note.text == "Note 3 text", User.email == "user2@example.com").first()
        if not note3:
            note3 = Note(
                id=str(uuid4()),
                text="Note 3 text",
                category="Category A",
                owner_id=user2.id,
            )
            db.add(note3)

        db.commit()

        # Partage des notes
        shared_note1 = db.query(UserNote).filter(UserNote.user_id == user2.id, UserNote.note_id == note1.id).first()
        if not shared_note1:
            shared_note1 = UserNote(
                user_id=user2.id,
                note_id=note1.id,
            )
            db.add(shared_note1)

        shared_note2 = db.query(UserNote).filter(UserNote.user_id == user1.id, UserNote.note_id == note3.id).first()
        if not shared_note2:
            shared_note2 = UserNote(
                user_id=user1.id,
                note_id=note3.id,
            )
            db.add(shared_note2)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error initializing the database: {e}")
    finally:
        db.close()
