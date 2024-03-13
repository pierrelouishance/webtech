from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from uuid import uuid4
from app.schemas.schemas import Book
import app.services.services as service
templates = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/books", tags=["Books"])
 
@router.get('/liste', response_class=HTMLResponse)
def get_books(request : Request):
    """
  Show books
    """
    books=service.get_all_books()
    return templates.TemplateResponse( request, "liste_books.html", context={"books": books})
def execute_function():
    print("ok")

@router.get('/update', response_class=HTMLResponse)
def get_update_book(request : Request):

    return templates.TemplateResponse( request, "update_books.html")


@router.get('/number')
def get_books_number():
    """
    Retrieve the total number of books.

    """
    books=service.get_all_books()
    number_books=len(books)
    return JSONResponse(
        content=number_books,
        status_code=200,
    )

@router.post('/add')
def create_new_book(name: str, auteur: str,editeur: str):
    """
    Create a new book.

    Args:
        name (str): The name of the book.
        auteur (str): The author of the book.
        editeur (str): The publisher of the book.

    Returns:
        JSONResponse: A JSON response containing the information of the new book.
    """
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
    return RedirectResponse(url="/books/liste")


@router.post('/delete/{book_id}')
def delete_book(book_id: str):
    """
    Delete a book by its ID.

    Args:
        book_id (str): The ID of the book to be deleted.

    Returns:
        JSONResponse: A JSON response indicating that the book has been deleted successfully.
    """
    
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )

    service.delete_book(book_id)
    response = RedirectResponse(url="/books/liste")
    response.status_code = 302
    return response


@router.post('/update/{book_id}')
def update_book(book_id: str, name: str = Form(...), auteur: str = Form(...), editeur: str = Form(...)):
    updated_book_data = {
        "id": book_id,
        "name": name,
        "auteur": auteur,
        "editeur": editeur
    }
    try:
        updated_book = Book(**updated_book_data)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book information structure.")

    service.update_book(book_id, updated_book)
    return RedirectResponse(url="/books/liste")