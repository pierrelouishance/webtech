
from fastapi import HTTPException
from app.database import Session
from app.models.books import Book
from uuid import uuid4
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from app.models.users import User
from werkzeug.security import generate_password_hash

from app.schemas.schemas import BookSchema
from app.schemas.users import UserSchema

def get_db():
    return Session()

def get_all_books():
    with get_db() as db:
        return db.query(Book).all()
    
def get_books_with_owners():
    with get_db() as db:
        return db.query(Book).options(joinedload(Book.owner)).all()

def get_available_books():
    with get_db() as db :
    # Récupère tous les livres qui ne sont pas vendus
        return db.query(Book).filter(Book.is_sale == "à vendre").all()


def get_book_by_id(id: str):
    with get_db() as db:
        book = db.query(Book).filter(Book.id == id).first()
        if book:
            return Book(
                id=book.id,
                name=book.name,
                auteur=book.auteur,
                editeur=book.editeur,
                prix=book.prix,
                is_sale=book.is_sale,
                owner_id=book.owner_id
            )
    return None



def delete_book(book_id: str, current_user: UserSchema):

    with get_db() as db:
        # Recherche du livre dans la base de données
        book = db.query(Book).filter(Book.id == book_id).first()

        if not book:
            # Si le livre n'est pas trouvé, lever une exception HTTP 404
            raise HTTPException(status_code=404, detail="Book not found.")

        # Vérifier si l'utilisateur est propriétaire du livre ou s'il est administrateur
        if current_user.role != "admin" and book.owner_id != current_user.id:
            # Si l'utilisateur n'est ni le propriétaire ni un administrateur, lever une exception HTTP 403 (interdit)
            raise HTTPException(status_code=403, detail="You are not authorized to delete this book.")

        # Suppression du livre de la base de données
        db.delete(book)
        db.commit()

def save_book(new_book: BookSchema, user : UserSchema):
    with get_db() as db:

        new_book_entity = Book(
            id = str(uuid4()),
            name = new_book.name,
            auteur = new_book.auteur,
            editeur = new_book.editeur,
            prix = new_book.prix,
            is_sale = new_book.is_sale,
            owner_id = user.id,
        )
        db.add(new_book_entity)
        db.commit()
        
def update_book(book_id: str, updated_data: BookSchema, current_user: UserSchema):
    with get_db() as db:
        # Récupère le livre à mettre à jour
        book = db.query(Book).filter(Book.id == book_id).first()

        if book is None:
            raise HTTPException(status_code=404, detail="Book not found.")

        # Vérifie si l'utilisateur est autorisé à mettre à jour le livre
        if current_user.role != "admin" and book.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="You are not authorized to update this book.")

        # Met à jour le livre avec les nouvelles données
        for key, value in updated_data.dict(exclude_unset=True).items():
            if hasattr(book, key):
                setattr(book, key, value)

        db.commit()
        db.refresh(book)


