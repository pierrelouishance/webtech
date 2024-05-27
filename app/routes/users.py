from fastapi import APIRouter, Query, status, Request, Form, Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.authentif.login_manager import login_manager
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
    response = RedirectResponse(url="/accueil?success= vous étes connecté en tant qu'utilisateur", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response
# Fonction utilitaire pour créer et définir un cookie d'authentification
def create_auth_cookie_login(user_id: str) -> RedirectResponse:
    access_token = login_manager.create_access_token(data={'sub': user_id})
    response = RedirectResponse(url="""/users/login?success=Votre compte a été crée avec succès
                                                        connectez-vous dès à présent !""", status_code=status.HTTP_302_FOUND)
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
        return RedirectResponse(url="/?error=vos identifiants sont incorrect", status_code=status.HTTP_302_FOUND)
    
    return create_auth_cookie(user.id)

#route pour afficher la page de connexion 
@router.get("/login")
def login_form(request: Request, user: UserSchema = Depends(login_manager)):
    return templates.TemplateResponse("login.html", {"request": request, "current_user": user})
# Route de création de compte
@router.post("/create")
def create_route_post(email: str = Form(None),name:str=Form(None), password: str = Form(None), confirm_password:str = Form(None)):
    
    if email is None  or name is None or password is None or confirm_password is None:
        # Si l'un des champs requis est manquant, rediriger vers la page de creation de page
        return RedirectResponse(url="/users/create", status_code=status.HTTP_303_SEE_OTHER)
    

    if password != confirm_password : 
        return RedirectResponse(url="/users/create?error=Les mots de passe ne correspondent pas", status_code=status.HTTP_303_SEE_OTHER)

    new_user_data = {
        "id": str(uuid4()),
        "email": email,
        "name": name,
        "password":password,
        "confirm_password" : confirm_password,
    }
    try:
        new_user = UserSchema(**new_user_data)
        create_user(new_user)

    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        # Si une ValidationError est levée (données invalides), rediriger vers la page d'erreur
    user = get_user_by_email(email)
    return create_auth_cookie_login(user.id)


# Route pour afficher le formulaire de création de compte
@router.get("/create")
def create_route_get(request: Request, user: UserSchema = Depends(login_manager.optional)):
    return templates.TemplateResponse("create_user.html", {"request": request,'current_user': user})

# Route de déconnexion
@router.post('/logout')
def logout_route():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(
        key=login_manager.cookie_name,
        httponly=True
    )
    return response

@router.get("/account")
def account_info(request: Request, current_user: UserSchema = Depends(login_manager)):
    return templates.TemplateResponse("account_info.html", {"request": request, "current_user": current_user})

@router.get("/account/update")
def update_account_form(request: Request, current_user: UserSchema = Depends(login_manager)):
    return templates.TemplateResponse("update_account.html", {"request": request, "current_user": current_user})

@router.post("/account/update")
def update_account(request: Request, current_user: UserSchema = Depends(login_manager),
                   name: str = Form(None), email: str = Form(None),
                   new_password: str = Form(None), confirm_password: str = Form(None)):

    # Vérifier si les nouveaux mots de passe correspondent
    if new_password != confirm_password:
        return RedirectResponse(url="/?error=Les mots de passe que vous avez saisi ne correspondent pas.", status_code=status.HTTP_302_FOUND)

    # Mettre à jour les informations de l'utilisateur
    current_user.name = name
    current_user.email = email

    # Hasher et mettre à jour le mot de passe uniquement s'il a été modifié
    if new_password.strip() != "":
        current_user.password = generate_password_hash(new_password)
        current_user.confirm_password = generate_password_hash(new_password)

    # Mettre à jour l'utilisateur dans la base de données
    update_user(current_user)

    # Rediriger l'utilisateur vers la page d'informations personnelles avec un message de succès
    return RedirectResponse(url="/?success=Votre mot de passe a été réinitialisé avec succès.", status_code=status.HTTP_302_FOUND)

@router.get("/password/reset/request")
def password_reset_request_form(request: Request):
    return templates.TemplateResponse("password_reset_request.html", {"request": request})

@router.post("/password/reset/request")
def password_reset_request(email: str = Form(None), name: str = Form(None), new_password: str = Form(None), confirm_password: str = Form(None)):
    if new_password != confirm_password:
        return RedirectResponse(url="/users/password/reset/request?error=Les mots de passe ne correspondent pas", status_code=status.HTTP_302_FOUND)
    
    user = get_user_by_email(email)
    if user is None or user.name != name:
        return RedirectResponse(url="/users/password/reset/request?error=Informations incorrectes", status_code=status.HTTP_302_FOUND)
    
    user.password = generate_password_hash(new_password)
    user.confirm_password = user.password  
    
    update_user(user)
    return RedirectResponse(url="""/?success=Votre mot de passe a été réinitialisé avec succès.
                                veuillez vous connecter à présent !""", status_code=status.HTTP_302_FOUND)
