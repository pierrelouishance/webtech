from fastapi import FastAPI, Request,Depends
from fastapi.staticfiles import StaticFiles
from app.routes.books import router as books_router
from app.routes.users import router as user_router
from app.schemas.users import  UserSchema
from app.login_manager import login_manager
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")



app = FastAPI(title="Books")
app.include_router(books_router)
app.include_router(user_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")

@app.get('/accueil')
def get_accueil(request: Request,
                user: UserSchema = Depends(login_manager.optional)):
    return templates.TemplateResponse("accueil.html", {"request": request,'current_user': user})

@app.get('/',)
def get_accueil(request: Request,
                user: UserSchema = Depends(login_manager.optional),):
    return templates.TemplateResponse("login.html", {"request": request,'current_user': user})