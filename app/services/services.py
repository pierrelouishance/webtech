from app.database import database
from app.schemas.schemas import Book
from fastapi import HTTPException

def get_all_books() -> list[Book]:
    """
    Get all books from the database.

    Returns:
        list[Book]: A list of Book objects representing all the books.
    """
    # Retrieving books data from the database and converting it into Book objects
    books_data = database["books"]
    books = [Book(**data) for data in books_data]
    return books

def save_book(new_book: Book) -> Book:
    """
    Save a new book to the database.

    Args:
        new_book (Book): The Book object representing the new book to be saved.

    Returns:
        Book: The saved Book object.
    """
    # Appending the dictionary representation of the new book to the database
    database["books"].append(new_book.dict())
    return new_book

def get_book_by_id(book_id: str):
    """
    Get a book by its ID from the database.

    Args:
        book_id (str): The ID of the book to retrieve.

    Returns:
        dict: The dictionary representation of the book if found, else None.
    """
    # Iterating through the books in the database to find the one with the specified ID
    for book in database["books"]:
        if book['id'] == book_id:
            return book
    return None

def delete_book(book_id: str):
    """
    Delete a book by its ID from the database.

    Args:
        book_id (str): The ID of the book to delete.

    Raises:
        HTTPException: If the book with the specified ID is not found.
    """
    # Getting the initial length of the books list in the database
    initial_length = len(database["books"])
    
    # Removing the book with the specified ID from the database
    database["books"] = [book for book in database["books"] if book["id"] != book_id]
    
    # Checking if the length of the books list has changed after deletion
    if initial_length == len(database["books"]):
        # If the length hasn't changed, raise an HTTP 404 error indicating that the book was not found
        raise HTTPException(
            status_code=404,
            detail="Book not found."
        )

def update_book(book_id: str, updated_book: Book):
    """
    Update a book's information in the database.

    Args:
        book_id (str): The ID of the book to update.
        updated_book (Book): The updated Book object with the new information.

    Raises:
        HTTPException: If the book with the specified ID is not found.
    """
    # Iterating through the books in the database to find the one with the specified ID
    for idx, book in enumerate(database["books"]):
        if book["id"] == book_id:
            # Updating the information of the book with the new data
            database["books"][idx] = updated_book.dict()
            return

    # If no book with the specified ID is found, raise an HTTP 404 error
    raise HTTPException(
        status_code=404,
        detail="Book not found."
    )
