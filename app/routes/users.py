from fastapi import APIRouter, HTTPException, status, Request, Form,Body,Depends
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from app.login_manager import login_manager
from app.services.users import *
from app.schemas.users import UserSchema

from uuid import uuid4
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/users")

@router.post("/login")
def login_route(email: str = Form(None), password: str = Form(None)):
    user = get_user_by_email(email)
    if user is None or user.password != password:
        return RedirectResponse(url="/users/create", status_code=status.HTTP_302_FOUND)
    access_token = login_manager.create_access_token(data={'sub': user.id})
    response = RedirectResponse(url="/accueil", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response


@router.post("/create")
def create_route_post(email: str = Form(None),prenom:str=Form(None),nom:str=Form(None), password: str = Form(None), role : str = Form(None)):
    if role is None:
        role = "client"

    new_user_data = {
        "id": str(uuid4()),
        "email": email,
        "prenom": prenom,
        "nom": nom,
        "password":password,
        "role": role 
    }
    try:

        new_user = UserSchema(**new_user_data)
        create_user(new_user)

    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        # Si une ValidationError est levée (données invalides), rediriger vers la page d'erreur
    user = get_user_by_email(email)
    if user is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials."
        )
    access_token = login_manager.create_access_token(
        data={'sub': user.id}
    )
    if user.role == "admin" :
        response = RedirectResponse(url="/users/userlist", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key=login_manager.cookie_name,
            value=access_token,
            httponly=True
        )
        return response
    else : 
        response = RedirectResponse(url="/users/userlist/client", status_code=status.HTTP_302_FOUND)
        response.set_cookie(
            key=login_manager.cookie_name,
            value=access_token,
            httponly=True
        )
        return response

@router.get("/create")
def create_route_get(request: Request, user: UserSchema = Depends(login_manager.optional)):
    return templates.TemplateResponse("create.html", {"request": request,'current_user': user})

@router.get("/userlist")
def get_admin_user_list(request: Request, user: UserSchema = Depends(login_manager.optional)):

    if user.role == "admin":
        users = get_all_users()
        return templates.TemplateResponse("user_list.html", {"request": request, "users": users, "current_user": user})

@router.get("/userlist/client")
def get_client_user_list(request: Request, user: UserSchema = Depends(login_manager.optional)):

    if user.role == "client":
        users = get_all_users()
        return templates.TemplateResponse("accueil.html", {"request": request, "users": users, "current_user": user})



@router.post('/logout')
def logout_route():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(
        key=login_manager.cookie_name,
        httponly=True
    )
    return response


@router.get("/me")
def current_user_route(
    user: UserSchema = Depends(login_manager),
):
    return user
