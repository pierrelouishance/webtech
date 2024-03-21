from fastapi import APIRouter, HTTPException, Response, status, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import ValidationError
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from app.schemas.schemas import Book
import app.services.services as service

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/books", tags=["Books"])


@router.get('/delete/{book_id}')
async def delete_book(book_id: str) -> RedirectResponse:
    """
    Delete a book by its ID.

    Args:
        book_id (str): The ID of the book to be deleted.

    Returns:
        RedirectResponse: Redirects to the list of books after successful deletion.
    """
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found.",
        )

    service.delete_book(book_id)
    return RedirectResponse(url="/books/liste", status_code=status.HTTP_302_FOUND)


@router.get('/number')
async def get_books_number() -> JSONResponse:
    """
    Retrieve the total number of books.

    Returns:
        JSONResponse: JSON response containing the number of books.
    """
    books = service.get_all_books()
    number_books = len(books)
    return JSONResponse(
        content={"number_of_books": number_books},
        status_code=status.HTTP_200_OK,
    )


@router.get("/add", response_class=HTMLResponse)
async def get_add_book(request: Request) -> HTMLResponse:
    """
    Render a page for adding a new book.

    Args:
        request (Request): The incoming request.

    Returns:
        HTMLResponse: HTML page for adding a new book.
    """
    return templates.TemplateResponse("add_book.html", {"request": request, "name": "", "auteur": "", "editeur": ""})




@router.post("/add", response_class=RedirectResponse)
async def create_new_book(name: str = Form(None), auteur: str = Form(None), editeur: str = Form(None)) -> RedirectResponse:
    if name is None or auteur is None or editeur is None:
        # Si tous les champs sont vides, redirigez vers la page d'erreur
        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)
    new_book_data = {
        "id": str(uuid4()),
        "name": name,
        "auteur": auteur,
        "editeur": editeur,
    }

    try:
        new_book = Book(**new_book_data)
        service.save_book(new_book)
        return RedirectResponse(url="/books/liste", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        # Si une ValidationError est levée (données invalides), rediriger vers la page d'erreur

        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)




@router.get("/error_add", response_class=HTMLResponse)
async def error_add_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("error_add.html", {"request": request})


@router.get("/book/edit/{book_id}", response_class=HTMLResponse)
async def edit_book(request: Request, book_id: str) -> HTMLResponse:
    """
    Render a page for editing a book.

    Args:
        request (Request): The incoming request.
        book_id (str): The ID of the book to be edited.

    Returns:
        HTMLResponse: HTML page for editing the book.
    """
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return templates.TemplateResponse("edit_book.html", {"request": request, "book": book})


@router.post("/update", response_class=RedirectResponse)
async def update_book(book_id: str = Form(None), name: str = Form(None), auteur: str = Form(None), editeur: str = Form(None)) -> RedirectResponse:
    """
    Update details of a book.

    Args:
        book_id (str): The ID of the book to be updated.
        name (str): The updated name of the book.
        auteur (str): The updated author of the book.
        editeur (str): The updated publisher of the book.

    Returns:
        RedirectResponse: Redirects to the list of books after successful update.
    """
    if book_id is None or name is None or auteur is None or editeur is None:
        # Si l'un des champs requis est manquant, rediriger vers la page d'erreur d'ajout
        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)

    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book.name = name
    book.auteur = auteur
    book.editeur = editeur

    try:
        service.update_book(book_id, book)
        return RedirectResponse(url="/books/liste", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)

@router.get('/liste')
async def get_books(request: Request) -> HTMLResponse:
    try:
        books = service.get_all_books()
        return templates.TemplateResponse("liste_books.html", context={ "request" : request , "books": books})

    except Exception as e:
        # Si une erreur se produit, vous pouvez la gérer ici
        # et renvoyer une réponse appropriée, par exemple une page d'erreur
        return templates.TemplateResponse("error_add.html", {"error_message": str(e)})

