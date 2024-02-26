from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from uuid import uuid4

from app.schemas.schemas import Book
import app.services.services as service



router = APIRouter(prefix="/books", tags=["Books"])
 
@router.get('/')
def get_books():
    books=service.get_all_books()
    return JSONResponse(
        content=[book.model_dump() for book in books],
        status_code=200,
    )
@router.get('/number')
def get_books_number():
    books=service.get_all_books()
    number_books=len(books)
    return JSONResponse(
        content=number_books,
        status_code=200,
    )

@router.post('/')
def create_new_book(name: str, auteur: str,editeur: str):
    new_book_data = {
        "id": str(uuid4()),
        "name": name,
        "auteur": auteur,
        "editeur" : editeur
    }
    try:
        new_book = Book.model_validate(new_book_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book information structure.",
        )
    
    service.save_book(new_book)
    return JSONResponse(new_book.model_dump())


@router.delete('/{book_id}')
def delete_book(book_id: str):
    # VÃ©rifier si le livre existe
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )
    # Supprimer le livre
    service.delete_book(book_id)
    return JSONResponse({"detail": "Book deleted successfully."})

@router.put('/{book_id}', description=" Used to Update Book")
def update_book(book_id: str, name: str, auteur: str, editeur: str):
    book = service.get_book_by_id(id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )

    book_data = {
        "id": book_id,
        "name": name,
        "auteur": auteur,
        "editeur": editeur
    }

    try:
        updated_book = Book.model_validate(book_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book information structure.",
        )

    service.update_book(book_id, updated_book)
    return JSONResponse(updated_book.model_dump())
