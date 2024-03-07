from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.schemas.schemas import Book
import app.services.services as service
templates = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/books", tags=["Books"])
 
@router.get('/liste')
def get_books(request : Request):
    """
  Show books
    """
    books=service.get_all_books()
    return templates.TemplateResponse(
request, "liste_books.html", context={"books": books})
def execute_function():
    print("ok")

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

@router.post('/')
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
    return JSONResponse(new_book.model_dump())


@router.post('/delete/{book_id}')
def delete_book(book_id: str,):
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


@router.put('/{book_id}', description="Update a book's information")
def update_book(book_id: str, name: str, auteur: str, editeur: str):
    """
    Update a book's information.

    Args:
        book_id (str): The ID of the book to be updated.
        name (str): The updated name of the book.
        auteur (str): The updated author of the book.
        editeur (str): The updated publisher of the book.

    Returns:
        JSONResponse: A JSON response containing the updated book's information.
    """
    # Creating a dictionary containing the updated information of the book
    updated_book_data = {
        "id": book_id,
        "name": name,
        "auteur": auteur,
        "editeur": editeur
    }
    try:
        # Validating the updated data with the Book model
        updated_book = Book(**updated_book_data)
    except ValidationError:
        # In case of validation error, return an HTTP 400 error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book information structure.",
        )

    # Calling the service function to update the book's information
    service.update_book(book_id, updated_book)
    # Returning a JSON response containing the updated book's information
    return JSONResponse(updated_book.model_dump())
