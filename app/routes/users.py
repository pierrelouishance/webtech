from fastapi import APIRouter, status, Request, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.login_manager import login_manager
from app.services.users import *
from app.schemas.users import UserSchema
from uuid import uuid4
from fastapi.templating import Jinja2Templates
from werkzeug.security import check_password_hash

templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/users")

# Fonction utilitaire pour créer et définir un cookie d'authentification
def create_auth_cookie(user_id: str) -> RedirectResponse:
    access_token = login_manager.create_access_token(data={'sub': user_id})
    response = RedirectResponse(url="/accueil", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response

# Route de connexion
@router.post("/login")
def login_route(email: str = Form(None), password: str = Form(None)):
    user = get_user_by_email(email)
    if user is None or not check_password_hash(user.password, password):
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    return create_auth_cookie(user.id)

# Route de création de compte
@router.post("/create")
def create_route_post(email: str = Form(None),prenom:str=Form(None),name:str=Form(None), password: str = Form(None), confirm_password:str = Form(None), role : str = Form(None)):
    
    if email is None or prenom is None or name is None or password is None or confirm_password is None:
        # Si l'un des champs requis est manquant, rediriger vers la page de creation de page
        return RedirectResponse(url="/users/create", status_code=status.HTTP_303_SEE_OTHER)
    
    if role is None:
        role = "client"

    if password != confirm_password : 
        return RedirectResponse(url="/users/create?error=Les mots de passe ne correspondent pas", status_code=status.HTTP_303_SEE_OTHER)

    new_user_data = {
        "id": str(uuid4()),
        "email": email,
        "prenom": prenom,
        "name": name,
        "password":password,
        "confirm_password" : confirm_password,
        "role": role 
    }
    try:
        new_user = UserSchema(**new_user_data)
        create_user(new_user)

    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        # Si une ValidationError est levée (données invalides), rediriger vers la page d'erreur
    user = get_user_by_email(email)
    return create_auth_cookie(user.id)

# Route pour afficher le formulaire de création de compte
@router.get("/create")
def create_route_get(request: Request, user: UserSchema = Depends(login_manager.optional)):
    return templates.TemplateResponse("create.html", {"request": request,'current_user': user})

# Route pour afficher la liste des utilisateurs
@router.get("/userlist")
def get_user_list(request: Request, user: UserSchema = Depends(login_manager.optional)):
    if user.role == "admin":
        users = get_all_users()
        return templates.TemplateResponse("user_list.html", {"request": request, "users": users, "current_user": user})
    else:
        # Rediriger le client vers l'accueil après la connexion
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)

# Route de déconnexion
@router.post('/logout')
def logout_route():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(
        key=login_manager.cookie_name,
        httponly=True
    )
    return response

# Route pour obtenir les informations de l'utilisateur actuel
@router.get("/me")
def current_user_route(user: UserSchema = Depends(login_manager)):
    return user
