from typing import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Form,Body,Depends
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from pydantic import ValidationError
from app.login_manager import login_manager
from app.services.users import get_user_by_username,create_user
from app.schemas.users import UserSchema
from uuid import uuid4
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
templates = Jinja2Templates(directory="templates")


router = APIRouter(prefix="/users")

@router.post("/login")
def login_route(
        username: str = Form(None), password: str = Form(None)
):
    user = get_user_by_username(username)
    if user is None or user.password != password:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials."
        )
    access_token = login_manager.create_access_token(
        data={'sub': user.id}
    )
    
    response = RedirectResponse(url="/accueil", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response


@router.post("/create")
def create_route_post(
        username: str = Form(None),prenom:str=Form(None),nom:str=Form(None), password: str = Form(None)
):
    

    new_user_data = {
        "id": str(uuid4()),
        "username": username,
        "prenom": prenom,
        "nom": nom,
        "password":password,
        "role":"client",
    }
    try:
        new_user = UserSchema(**new_user_data)
        create_user(new_user)


    except ValidationError as e:
        error_message = ", ".join([f"{error['loc'][-1]}: {error['msg']}" for error in e.errors()])
        # Si une ValidationError est levée (données invalides), rediriger vers la page d'erreur
    user = get_user_by_username(username)
    if user is None:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad credentials."
        )
    access_token = login_manager.create_access_token(
        data={'sub': user.id}
    )
    
    response = RedirectResponse(url="/accueil", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key=login_manager.cookie_name,
        value=access_token,
        httponly=True
    )
    return response

@router.get("/create")
def create_route_get(request: Request,
                user: UserSchema = Depends(login_manager.optional),):
    return templates.TemplateResponse("create.html", {"request": request,'current_user': user})


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
