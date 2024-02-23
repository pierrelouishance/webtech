from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from uuid import uuid4

from app.schemas.schemas import Book
import app.services.services as service



router = APIRouter(prefix="/books", tags=["First"])
 
@router.get('/')
def get_books():
    books=service.get_all_books()
    return JSONResponse(
        content=[book.model_dump() for book in books],
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
    