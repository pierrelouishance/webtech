from app.database import database
from app.schemas.schemas import Book
from fastapi import HTTPException, status


def get_all_books() -> list[Book]:
    books_data = database["books"]
    books = [Book(**data) for data in books_data]
    return books

def save_book(new_book: Book) -> Book:
    database["books"].append(new_book.dict())
    return new_book

def get_book_by_id(book_id: str):
    for book in database["books"]:
        if book['id'] == book_id:
            return book
    return None

def delete_book(book_id: str):
    global database
    database["books"] = [book for book in database["books"] if book["id"] != book_id]

def update_book(book_id: str, updated_book: Book):
    for idx, book in enumerate(database["books"]):
        if book["id"] == book_id:
            # Mettre à jour les informations du livre avec les nouvelles données
            database["books"][idx] = updated_book
            return

    # Si aucun livre correspondant à l'identifiant n'est trouvé, lever une exception
    raise ValueError("Book not found.")
