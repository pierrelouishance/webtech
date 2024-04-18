
from fastapi import HTTPException
from app.database import Session
from app.models.books import Book
from app.models.users import User
from werkzeug.security import generate_password_hash

def get_db():
    return Session()

def get_all_books():
    with get_db() as db:
        return db.query(Book).all()

def get_book_by_id(id: str):
    with get_db() as db:
        return db.query(Book).filter(Book.id == id).first()

def create_book(user_id: int, book_data: dict):
    with Session() as db:
        new_book = Book(**book_data, owner_id=user_id)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    
def delete_book(id: str):
    with get_db() as db:
        db_book = db.query(Book).filter(Book.id == id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        db.delete(db_book)
        db.commit()

def update_book(id: str, updated_book: Book):
    with get_db() as db:
        db_book = db.query(Book).filter(Book.id == id).first()
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        for key, value in updated_book.dict().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book