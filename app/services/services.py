from app.database import database
# from app.schemas import Book
from app.schemas.schemas import Book


def get_all_books()  -> list[Book]:  # (retirer les deux points après la fonction quand retirera le #) : fait
    books_data = database["books"]
    books = [Book.model_validate(data) for data in books_data] # (remplacer la fonction du dessous par celle ci
    return books

def save_book(new_book: Book) -> Book:
    database["books"].append(new_book)
    return new_book
