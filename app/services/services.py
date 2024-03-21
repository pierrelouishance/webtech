from app.database import database
# from app.schemas import Book
from app.schemas.schemas import Book
from fastapi import APIRouter, HTTPException, status


def get_all_books()  -> list[Book]:  
    """
    Get all books from the database.

    Returns:
        list[Book]: A list of Book objects representing all the books.
    """    

    books_data = database["books"]
    books = [Book.model_validate(data) for data in books_data] 
    return books

def save_book(new_book: Book) -> Book:
    """
    Save a new book to the database.

    Args:
        new_book (Book): The Book object representing the new book to be saved.

    Returns:
        Book: The saved Book object.
    """
    book_dict = new_book.dict()  # Conversion de l'objet Pydantic en dictionnaire
    database["books"].append(book_dict)
    return new_book



def get_book_by_id(book_id: str):
    """
    Get a book by its ID from the database.

    Args:
        book_id (str): The ID of the book to retrieve.

    Returns:
        Book: The Book object if found, else None.
    """
    for book_data in database["books"]:
        if book_data['id'] == book_id:
            return Book(**book_data)  # Create a Book object from the dictionary
    return None
def delete_book(book_id: str):
    """
    Delete a book by its ID from the database.

    Args:
        book_id (str): The ID of the book to delete.

    Raises:
        HTTPException: If the book with the specified ID is not found.
    """
    global database

    book_index = None
    for i, book in enumerate(database["books"]):
        if book['id'] == book_id:
            book_index = i
            break

    if book_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )


    del database["books"][book_index]

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