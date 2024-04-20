from fastapi import APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import ValidationError
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from app.models.users import User
from app.models.books import Book
from app.schemas.schemas import BookSchema
from app.schemas.users import UserSchema
from app.services import services as service
from app.login_manager import login_manager

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/books", tags=["Books"])


@router.get('/delete/{book_id}', response_class=RedirectResponse)
async def delete_book(book_id: str, user: UserSchema = Depends(login_manager)) -> RedirectResponse:

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete books.")
    
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found.",
        )

    service.delete_book(book_id, user)
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
async def get_add_book(request: Request, user: User = Depends(login_manager)) -> HTMLResponse:
    return templates.TemplateResponse("add_book.html", {"current_user":user,"request": request, "name": "", "auteur": "", "editeur": "", "prix" : "", "is_sale": ""})
@router.post("/add", response_class=RedirectResponse)
async def create_new_book(user: UserSchema = Depends(login_manager), name: str = Form(None), auteur: str = Form(None), editeur: str = Form(None), prix: float = Form(None), is_sale: str = Form(None)) -> RedirectResponse:
    
    if name is None or auteur is None or editeur is None:
        # Si tous les champs sont vides, redirigez vers la page d'erreur
        return RedirectResponse(url="/books/add", status_code=status.HTTP_303_SEE_OTHER)
    if is_sale is None : 
        is_sale = "à vendre"

    new_book_data = {
        "id" : str(uuid4()),
        "name": name,
        "auteur": auteur,
        "editeur": editeur,
        "prix" : prix,
        "is_sale" : is_sale,
        "owner_id" : user.id,
    }
    try:
        new_book = BookSchema.model_validate(new_book_data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid information for the book.",
        )

    try:
        service.save_book(new_book, user)
        return RedirectResponse(url="/books/liste", status_code=status.HTTP_303_SEE_OTHER)
    except IntegrityError:
        # Gérer l'erreur de contrainte d'unicité
        return RedirectResponse(url="/books/error_add?message=Book name already exists", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/error_add", response_class=HTMLResponse)
async def error_add_page(request: Request, user: UserSchema = Depends(login_manager.optional)) -> HTMLResponse:
    return templates.TemplateResponse("error_add.html", {"request": request , "current_user":user})


@router.get("/book/edit/{book_id}", response_class=HTMLResponse)
async def edit_book(request: Request, book_id: str,user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return templates.TemplateResponse("edit_book.html", {"current_user": user,"request": request, "book": book})


@router.post("/update", response_class=RedirectResponse)
async def update_book(
    book_id: str = Form(None),  
    user: UserSchema = Depends(login_manager),  
    name: str = Form(None), 
    auteur: str = Form(None), 
    editeur: str = Form(None),
    prix: float = Form(None),
    is_sale: str = Form(None),
    owner_id : str = Form(None)  ) -> RedirectResponse:

    if book_id is None or name is None or auteur is None or editeur is None or prix is None or is_sale is None or owner_id is None:
        # Si l'un des champs requis est manquant, rediriger vers la page d'erreur d'ajout
        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)
    


    book = service.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    updated_data = BookSchema(
        id = book_id ,
        name=name, 
        auteur=auteur, 
        editeur=editeur,
        prix = prix,
        is_sale = is_sale,
        owner_id=owner_id
        )

    try:
        service.update_book(book_id, updated_data, user)
        return RedirectResponse(url="/books/liste", status_code=status.HTTP_302_FOUND)
    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        return RedirectResponse(url="/books/error_add", status_code=status.HTTP_303_SEE_OTHER)

@router.get('/liste')
async def get_books(request: Request, user: UserSchema = Depends(login_manager.optional)) -> HTMLResponse:
    try: 
        books = service.get_books_with_owners()
        return templates.TemplateResponse("liste_books.html", context={ "request" : request , "books": books,"current_user":user})

    except Exception as e:
        # Si une erreur se produit, vous pouvez la gérer ici
        # et renvoyer une réponse appropriée, par exemple une page d'erreur
        return templates.TemplateResponse("error_add.html", {"error_message": str(e)})

