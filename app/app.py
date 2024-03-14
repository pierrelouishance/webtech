from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.books import router as books_router

from fastapi import APIRouter, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Books")
app.include_router(books_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")


@app.get('/',)
def get_accueil(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request})
    
