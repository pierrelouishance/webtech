from fastapi import APIRouter, HTTPException, status, Request, Form, Depends
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import ValidationError
from uuid import uuid4
from sqlalchemy.exc import IntegrityError
from fastapi.templating import Jinja2Templates
from app.models.users import User
from app.schemas.notes import NoteSchema
from app.schemas.types import NoteShareSchema
from app.schemas.users import UserSchema
from app.services import notes as note
from app.authentif.login_manager import login_manager
from app.services.types import get_shared_notes, share_note_with_user
from app.services.users import get_all_users

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get('/liste')
async def get_books(request: Request, user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    try: 
        notes = note.get_notes_with_owners()
        return templates.TemplateResponse("liste_notes.html", context={ "request" : request , "notes": notes,"current_user":user})

    except Exception as e:
        # Si une erreur se produit, vous pouvez la gérer ici
        # et renvoyer une réponse appropriée, par exemple une page d'erreur
        return templates.TemplateResponse("error.html", {"error_message": str(e)})
    

@router.get("/add", response_class=HTMLResponse)
async def get_add_note(request: Request, user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    categories = ["Travail", "Personnel", "Étude", "Divertissement", "Autre"] 
    return templates.TemplateResponse("add_note.html", {"current_user": user, "request": request, "text": "", "categories": categories})


@router.post("/add", response_class=RedirectResponse)
async def create_new_note(user: UserSchema = Depends(login_manager), text: str = Form(None), category: str = Form(None)) -> RedirectResponse:
    
    if text is None or category is None:
        # Si tous les champs sont vides, redirigez vers la page d'erreur
        return RedirectResponse(url="/notes/add", status_code=status.HTTP_303_SEE_OTHER)

    new_note_data = {
        "id": str(uuid4()),
        "text": text,
        "category": category,
        "owner_id": user.id,
    }

    try:
        new_note = NoteSchema.model_validate(new_note_data)
        note.save_note(new_note, user)
        return RedirectResponse(url="/notes/liste", status_code=status.HTTP_303_SEE_OTHER)
    except ValidationError:
        # Gérer l'erreur de validation
        return RedirectResponse(url="/notes/error_add?message=Invalid information for the note", status_code=status.HTTP_303_SEE_OTHER)
    except IntegrityError:
        # Gérer l'erreur de contrainte d'unicité
        return RedirectResponse(url="/notes/error_add?message=Note already exists", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/error_add", response_class=HTMLResponse)
async def error_add_page(request: Request, user: UserSchema = Depends(login_manager.optional)) -> HTMLResponse:
    return templates.TemplateResponse("error_add.html", {"request": request , "current_user":user}) 


@router.get("/mes_notes", response_class=HTMLResponse)
async def get_user_notes_route(request: Request, current_user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    user_notes = note.get_user_notes(current_user.id)
    return templates.TemplateResponse("mes_notes.html", {"request": request, "current_user": current_user, "user_notes": user_notes})

@router.get('/delete/{note_id}', response_class=RedirectResponse)
async def delete_note(note_id: str, user: UserSchema = Depends(login_manager)) -> RedirectResponse:

    try:
        note.delete_note(note_id, user.id)
        return RedirectResponse(url="/notes/mes_notes", status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        return RedirectResponse(url="/notes/error_add", status_code=status.HTTP_404_NOT_FOUND)
    
@router.get("/edit/{note_id}")
async def update_note_form(request: Request, note_id: str, current_user: User = Depends(login_manager)):

    notes = note.get_note_by_id(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note non trouvée")
    return templates.TemplateResponse("edit_note.html", {"request": request, "current_user": current_user, "note": notes})

@router.post("/edit/{note_id}")
def update_note_post(request: Request, note_id: str, current_user: UserSchema = Depends(login_manager),
                     text: str = Form(None), category: str = Form(None)):
    note.update_note(note_id, current_user.id, text, category)
    return RedirectResponse(url=f"/accueil?success=Note mise à jour avec succès.", status_code=status.HTTP_302_FOUND)

@router.get("/partager", response_class=HTMLResponse)
async def get_share_note_form(request: Request, user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    users = get_all_users()
    user_notes = note.get_user_notes(user.id)
    return templates.TemplateResponse("partage.html", {"request": request, "current_user": user, "users": users, "user_notes": user_notes})

@router.post("/partager", response_class=RedirectResponse)
async def partager_une_note(note_id: str = Form(None), user_id: str = Form(None), current_user: UserSchema = Depends(login_manager)) -> RedirectResponse:
    note_share_data = NoteShareSchema(note_id=note_id, user_id=user_id)
    share_note_with_user(note_share_data)
    return RedirectResponse(url="/notes/liste", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/partagees", response_class=HTMLResponse)
async def get_notes_partagees(request: Request, current_user: UserSchema = Depends(login_manager)) -> HTMLResponse:
    notes = get_shared_notes(current_user.id)
    return templates.TemplateResponse("note_partagee.html", {"request": request, "current_user": current_user, "notes": notes})
