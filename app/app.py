from fastapi import Depends, FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from app.database.database import create_database
from app.authentif.login_manager import login_manager
from app.database.init_db import init_db
from app.routes.notes import router as notes_router
from app.routes.users import router as users_router
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.schemas.users import UserSchema


templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Notes")
app.include_router(notes_router)
app.include_router(users_router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event('startup')
def on_application_started():
    create_database()
    init_db()  
    
def on_shutdown():
    print("Bye bye!")

# # Route for the home page
# @app.get('/accueil')
# def get_accueil(request: Request,
#                 user: UserSchema = Depends(login_manager.optional)):
#     return templates.TemplateResponse("accueil.html", {"request": request,'current_user': user})

@app.get('/')
def get_accueil(request: Request,
                user: UserSchema = Depends(login_manager.optional),):
    return templates.TemplateResponse("login.html", {"request": request,'current_user': user})
    
