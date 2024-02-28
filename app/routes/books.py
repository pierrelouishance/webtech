from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from uuid import uuid4

# Importing the Book model from the schemas module
from app.schemas.schemas import Book

# Importing service functions to manipulate books
import app.services.services as service

# Creating a router for operations related to books
router = APIRouter(prefix="/books", tags=["Books"])

# Route to get all books
@router.get('/', description="Get all books")
def get_books():
    """
    Retrieve all books.

    Returns:
        JSONResponse: A JSON response containing the list of books.
    """
    # Calling the service function to get all books
    books = service.get_all_books()
    # Returning a JSON response containing the books as a dictionary
    return JSONResponse(
        content=[book.model_dump() for book in books],  # Using the model_dump method for each book
        status_code=200,
    )

# Route to get the total number of books
@router.get('/number', description="Get the total number of books")
def get_books_number():
    """
    Retrieve the total number of books.

    Returns:
        JSONResponse: A JSON response containing the number of books.
    """
    # Calling the service function to get all books
    books = service.get_all_books()
    # Calculating the total number of books
    number_books = len(books)
    # Returning a JSON response containing the number of books
    return JSONResponse(
        content=number_books,
        status_code=200,
    )

# Route to create a new book
@router.post('/', description="Create a new book")
def create_new_book(name: str, auteur: str, editeur: str):
    """
    Create a new book.

    Args:
        name (str): The name of the book.
        auteur (str): The author of the book.
        editeur (str): The publisher of the book.

    Returns:
        JSONResponse: A JSON response containing the information of the new book.
    """
    # Creating a new book with a randomly generated ID
    new_book_data = {
        "id": str(uuid4()),  # Generating a new ID
        "name": name,
        "auteur": auteur,
        "editeur": editeur
    }
    try:
        # Validating the data of the new book with the Book model
        new_book = Book(**new_book_data)
    except ValidationError:
        # In case of validation error, return an HTTP 400 error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid book information structure.",
        )
    
    # Calling the service function to save the new book
    service.save_book(new_book)
    # Returning a JSON response containing the information of the new book
    return JSONResponse(new_book.model_dump())

# Route to delete a book by its ID
@router.delete('/{book_id}', description="Delete a book by its ID")
def delete_book(book_id: str):
    """
    Delete a book by its ID.

    Args:
        book_id (str): The ID of the book to be deleted.

    Returns:
        JSONResponse: A JSON response indicating that the book has been deleted successfully.
    """
    # Calling the service function to delete the book with the specified ID
    service.delete_book(book_id)
    # Returning a JSON response indicating that the book has been deleted successfully
    return JSONResponse({"detail": "Book deleted successfully."})

# Route to update a book's information
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
    # updated_book_data = {
    #     "id": book_id,
    #     "name": name,
    #     "auteur": auteur,
    #     "editeur": editeur
    # }
    try:
        # Validating the updated data with the Book model
        # updated_book = Book(**updated_book_data)
        updated_book = Book(
            id=book_id,
            name=name,
            auteur=auteur,
            editeur=editeur,
        )
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
