from app.database import database
# from app.schemas import Book
from app.schemas.schemas import Book
from fastapi import APIRouter, HTTPException, status


def get_all_books()  -> list[Book]:  
    books_data = database["books"]
    books = [Book.model_validate(data) for data in books_data] 

def save_book(new_book: Book) -> Book:
    database["books"].append(new_book)
    return new_book


def get_book_by_id(book_id: str):
    for book in database["books"]:
        if book['id'] == book_id:
            return book
    return None
def delete_book(book_id: str):
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


