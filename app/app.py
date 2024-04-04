from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from app.routes.books import router as books_router
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError


templates = Jinja2Templates(directory="templates")


app = FastAPI(title="Books")

app.mount("/static", StaticFiles(directory="static"), name="static")

# Register routes
app.include_router(books_router)
app.include_router(users.router)

@app.on_event('startup')
def on_startup():
    print("Server started.")


def on_shutdown():
    print("Bye bye!")

# Route for the home page
@app.get('/',)
def get_accueil(request: Request):
    return templates.TemplateResponse("accueil.html", {"request": request})

# Route for handling 404 errors
@app.exception_handler(404)
async def not_found(request: Request, exc: Exception):
    return RedirectResponse("/", status_code=303)
    
